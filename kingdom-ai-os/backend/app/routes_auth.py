from __future__ import annotations

import asyncio

from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, Field

from app.services import auth

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])


def client_ip(request: Request) -> str:
    return request.headers.get("x-real-ip") or (request.client.host if request.client else "unknown")


def _set_cookie(response: Response, request: Request) -> None:
    secure = request.headers.get("x-forwarded-proto", request.url.scheme) == "https"
    response.set_cookie(auth.SESSION_COOKIE, auth.new_session(), max_age=int(auth.SESSION_HOURS * 3600),
                        httponly=True, samesite="strict", secure=secure, path="/")


class LoginIn(BaseModel):
    password: str = Field(max_length=256)
    code: str = Field(default="", max_length=12)


class SetupIn(BaseModel):
    setup_token: str = Field(max_length=512)
    code: str = Field(default="", max_length=12)


class ChangeIn(BaseModel):
    current_password: str = Field(max_length=256)
    new_password: str = Field(min_length=12, max_length=256)
    code: str = Field(max_length=12)


@router.get("/status")
async def status(request: Request):
    on = auth.enabled()
    return {"enabled": on or auth.required_but_missing(), "configured": on,
            "authenticated": (not on and not auth.required_but_missing()) or auth.valid_session(request.cookies.get(auth.SESSION_COOKIE)),
            "two_factor": auth.totp_ready()}


async def _guard(request: Request) -> str:
    ip = client_ip(request)
    wait = auth.locked(ip)
    if wait:
        raise HTTPException(429, f"Too many wrong tries. Try again in {wait // 60 + 1} minutes.")
    return ip


async def _fail(ip: str, msg: str):
    auth.record_fail(ip)
    await asyncio.sleep(0.8)  # slows down guessing
    raise HTTPException(401, msg)


@router.post("/login")
async def login(payload: LoginIn, request: Request, response: Response):
    if not auth.enabled():
        raise HTTPException(503, "Login is not configured on this server yet.")
    ip = await _guard(request)
    if not auth.check_password(payload.password):
        await _fail(ip, "Wrong password or code.")
    if not auth.totp_ready():
        auth.clear_fails(ip)
        return {"ok": False, "setup_required": True, "setup_token": auth.new_setup_token()}
    if not payload.code.strip():
        return {"ok": False, "code_required": True}
    if not auth.verify_code(payload.code):
        await _fail(ip, "Wrong password or code.")
    auth.clear_fails(ip)
    _set_cookie(response, request)
    return {"ok": True}


@router.post("/totp/start")
async def totp_start(payload: SetupIn, request: Request):
    await _guard(request)
    if auth.totp_ready() or not auth.valid_setup_token(payload.setup_token):
        raise HTTPException(403, "Setup link expired. Sign in with your password again.")
    return auth.start_totp_setup()


@router.post("/totp/confirm")
async def totp_confirm(payload: SetupIn, request: Request, response: Response):
    ip = await _guard(request)
    if auth.totp_ready() or not auth.valid_setup_token(payload.setup_token):
        raise HTTPException(403, "Setup link expired. Sign in with your password again.")
    if not auth.confirm_totp_setup(payload.code):
        await _fail(ip, "That code didn't match. Check the time on your phone and try the newest code.")
    auth.clear_fails(ip)
    _set_cookie(response, request)
    return {"ok": True}


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(auth.SESSION_COOKIE, path="/")
    return {"ok": True}


@router.post("/change-password")
async def change_password(payload: ChangeIn, request: Request, response: Response):
    if not auth.valid_session(request.cookies.get(auth.SESSION_COOKIE)):
        raise HTTPException(401, "Sign in first.")
    ip = await _guard(request)
    if not auth.check_password(payload.current_password) or not auth.verify_code(payload.code):
        await _fail(ip, "Wrong password or code.")
    auth.change_password(payload.new_password)
    _set_cookie(response, request)
    return {"ok": True}
