"""Optional Convex real-time state emitter (bridges Postgres + Redis state events to Convex when configured)."""

from __future__ import annotations

from typing import Dict

import httpx

from . import config


async def emit_convex_event(event_type: str, payload: Dict[str, str]) -> bool:
    """Emit non-blocking state change event to Convex webhook if CONVEX_WEBHOOK_URL is set."""
    url = config.SETTINGS.convex_webhook_url.strip()
    if not url:
        return False
    try:
        async with httpx.AsyncClient(timeout=2.5) as client:
            res = await client.post(url, json={"event": event_type, "payload": payload})
            return res.status_code < 300
    except Exception:
        return False
