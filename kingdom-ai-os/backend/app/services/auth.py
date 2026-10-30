"""Login for Kingdom AI OS: password + authenticator-app code (TOTP, RFC 6238).

Nothing secret lives in git. The server keeps its own state in the data volume:
  - session signing key (random, made on first start)
  - the authenticator secret (made on the server when the owner first signs in)
  - an optional new password hash (when the owner changes the password)
The first password comes from KAIOS_PASSWORD_HASH (a PBKDF2 hash) or KAIOS_PASSWORD.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import struct
import threading
import time
from pathlib import Path
from typing import Any
from urllib.parse import quote

SESSION_COOKIE = "kaios_session"
SESSION_HOURS = float(os.getenv("KAIOS_SESSION_HOURS", "12"))
MAX_FAILS = 5            # per IP before lockout
LOCK_SECONDS = 15 * 60
GLOBAL_MAX_FAILS = 30    # all IPs together, per lock window
PBKDF2_ROUNDS = 600_000
ISSUER = "Kingdom AI OS"

_lock = threading.Lock()
_fails: dict[str, list[float]] = {}


def _state_path() -> Path:
    db = os.getenv("KAIOS_DB_PATH", "")
    base = Path(db).parent if db else Path(os.getenv("KAIOS_DATA_DIR", "data"))
    return base / "auth.json"


def _load() -> dict[str, Any]:
    p = _state_path()
    try:
        return json.loads(p.read_text("utf-8"))
    except (OSError, ValueError):
        return {}


def _save(state: dict[str, Any]) -> None:
    p = _state_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(state), "utf-8")
    os.chmod(tmp, 0o600)
    tmp.replace(p)


def _state() -> dict[str, Any]:
    with _lock:
        s = _load()
        if not s.get("key"):
            s["key"] = secrets.token_hex(32)
            _save(s)
        return s


def _update(**changes: Any) -> dict[str, Any]:
    with _lock:
        s = _load()
        s.update(changes)
        _save(s)
        return s


# ---------- passwords ----------
def hash_password(password: str, rounds: int = PBKDF2_ROUNDS) -> str:
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, rounds)
    return f"pbkdf2_sha256${rounds}${salt.hex()}${dk.hex()}"


def _check_hash(password: str, stored: str) -> bool:
    try:
        algo, rounds, salt, digest = stored.replace(":", "$").split("$")
        if algo != "pbkdf2_sha256":
            return False
        dk = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), int(rounds))
        return hmac.compare_digest(dk.hex(), digest)
    except (ValueError, TypeError):
        return False


def _password_source() -> str | None:
    s = _load()
    if s.get("password_hash"):
        return s["password_hash"]
    if os.getenv("KAIOS_PASSWORD_HASH", "").strip():
        return os.getenv("KAIOS_PASSWORD_HASH", "").strip()
    if os.getenv("KAIOS_PASSWORD", ""):
        return "plain$" + os.getenv("KAIOS_PASSWORD", "")
    return None


def enabled() -> bool:
    return _password_source() is not None


def required_but_missing() -> bool:
    """Production with no password configured: lock the API instead of leaving it open."""
    return not enabled() and os.getenv("APP_ENV", "development").lower() == "production"


def check_password(password: str) -> bool:
    src = _password_source()
    if not src or not password:
        return False
    if src.startswith("plain$"):
        return hmac.compare_digest(src[6:].encode(), password.encode())
    return _check_hash(password, src)


# ---------- TOTP ----------
def new_totp_secret() -> str:
    return base64.b32encode(secrets.token_bytes(20)).decode().rstrip("=")


def totp(secret: str, counter: int, digits: int = 6) -> str:
    key = base64.b32decode(secret + "=" * (-len(secret) % 8), casefold=True)
    h = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    o = h[-1] & 0x0F
    code = (struct.unpack(">I", h[o:o + 4])[0] & 0x7FFFFFFF) % 10 ** digits
    return str(code).zfill(digits)


def _match_code(secret: str, code: str, now: float | None = None) -> int | None:
    code = "".join(ch for ch in str(code or "") if ch.isdigit())
    if len(code) != 6:
        return None
    t = int((now or time.time()) // 30)
    for c in (t - 1, t, t + 1):
        if hmac.compare_digest(totp(secret, c), code):
            return c
    return None


def verify_code(code: str) -> bool:
    """Checks the authenticator code and refuses a code that was already used."""
    s = _load()
    secret = s.get("totp_secret")
    if not secret or not s.get("totp_confirmed"):
        return False
    c = _match_code(secret, code)
    if c is None or c <= int(s.get("totp_last", 0)):
        return False
    _update(totp_last=c)
    return True


def totp_ready() -> bool:
    s = _load()
    return bool(s.get("totp_secret") and s.get("totp_confirmed"))


def start_totp_setup() -> dict[str, str]:
    s = _load()
    secret = s.get("pending_totp") or new_totp_secret()
    _update(pending_totp=secret)
    uri = f"otpauth://totp/{quote(ISSUER)}:owner?secret={secret}&issuer={quote(ISSUER)}&digits=6&period=30"
    return {"secret": secret, "uri": uri, "qr_svg": _qr_svg(uri)}


def confirm_totp_setup(code: str) -> bool:
    s = _load()
    pending = s.get("pending_totp")
    if not pending:
        return False
    c = _match_code(pending, code)
    if c is None:
        return False
    _update(totp_secret=pending, totp_confirmed=True, totp_last=c, pending_totp=None)
    return True


def _qr_svg(data: str) -> str:
    try:
        import segno
        import io
        buf = io.BytesIO()
        segno.make(data, error="m").save(buf, kind="svg", scale=6, border=2, dark="#111", light="#fff")
        return "data:image/svg+xml;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:  # pragma: no cover - the text secret still works
        return ""


# ---------- sessions ----------
def _sign(payload: dict[str, Any]) -> str:
    body = base64.urlsafe_b64encode(json.dumps(payload, separators=(",", ":")).encode()).decode().rstrip("=")
    sig = hmac.new(bytes.fromhex(_state()["key"]), body.encode(), hashlib.sha256).hexdigest()
    return f"{body}.{sig}"


def _unsign(token: str | None, kind: str) -> dict[str, Any] | None:
    if not token or "." not in token:
        return None
    body, sig = token.rsplit(".", 1)
    good = hmac.new(bytes.fromhex(_state()["key"]), body.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(sig, good):
        return None
    try:
        data = json.loads(base64.urlsafe_b64decode(body + "=" * (-len(body) % 4)))
    except ValueError:
        return None
    if data.get("k") != kind or float(data.get("exp", 0)) < time.time():
        return None
    return data


def new_session() -> str:
    return _sign({"k": "session", "exp": time.time() + SESSION_HOURS * 3600, "n": secrets.token_hex(8)})


def valid_session(token: str | None) -> bool:
    return _unsign(token, "session") is not None


def new_setup_token() -> str:
    """Short pass (10 min) that only allows setting up the authenticator after a correct password."""
    return _sign({"k": "setup", "exp": time.time() + 600})


def valid_setup_token(token: str | None) -> bool:
    return _unsign(token, "setup") is not None


def rotate_key() -> None:
    """Signs everyone out (used after a password change)."""
    _update(key=secrets.token_hex(32))


def change_password(new_password: str) -> None:
    _update(password_hash=hash_password(new_password))
    rotate_key()


# ---------- brute-force protection ----------
def locked(ip: str) -> int:
    """Seconds left on a lockout for this IP (0 = not locked)."""
    now = time.time()
    with _lock:
        for k in list(_fails):
            _fails[k] = [t for t in _fails[k] if now - t < LOCK_SECONDS]
            if not _fails[k]:
                del _fails[k]
        mine = _fails.get(ip, [])
        total = sum(len(v) for v in _fails.values())
        if len(mine) >= MAX_FAILS:
            return int(LOCK_SECONDS - (now - mine[0])) + 1
        if total >= GLOBAL_MAX_FAILS:
            oldest = min(t for v in _fails.values() for t in v)
            return int(LOCK_SECONDS - (now - oldest)) + 1
    return 0


def record_fail(ip: str) -> None:
    with _lock:
        _fails.setdefault(ip, []).append(time.time())


def clear_fails(ip: str) -> None:
    with _lock:
        _fails.pop(ip, None)


def reset_for_tests() -> None:
    with _lock:
        _fails.clear()
