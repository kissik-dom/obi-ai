"""Kingdom AI OS security middleware.

Adds request IDs, security headers, cheap path allow-listing, and a turn-off
flag. Deeper WAF/SIEM inspection is delegated to the edge security compose.
"""
from __future__ import annotations

import os
import time
import uuid
from typing import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse


class KingdomSecurityMiddleware(BaseHTTPMiddleware):
    """Security headers and idempotency/request-id normalization."""

    def __init__(self, app, **kwargs):
        super().__init__(app, **kwargs)
        self.enabled = os.getenv("FLAG_SECURITY_MIDDLEWARE", "1") == "1"
        self.max_body_bytes = int(os.getenv("MAX_BODY_BYTES", "25_000_000"))

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        request_id = request.headers.get("x-request-id", uuid.uuid4().hex)

        if not self.enabled:
            response = await call_next(request)
            response.headers["x-request-id"] = request_id
            return response

        content_length = request.headers.get("content-length")
        if content_length and content_length.isdigit() and int(content_length) > self.max_body_bytes:
            return JSONResponse({"detail": "payload too large", "max_body_bytes": self.max_body_bytes}, status_code=413)

        started = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = round((time.perf_counter() - started) * 1000, 3)
        response.headers["x-request-id"] = request_id
        response.headers["x-content-type-options"] = "nosniff"
        response.headers["x-frame-options"] = "DENY"
        response.headers["referrer-policy"] = "no-referrer"
        response.headers["permissions-policy"] = "camera=(self), geolocation=(), microphone=(self)"
        if request.url.path in {"/docs", "/redoc"}:
            response.headers["content-security-policy"] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
                "img-src 'self' data: https://fastapi.tiangolo.com; "
                "font-src 'self' data: https://cdn.jsdelivr.net; "
                "frame-ancestors 'none'; base-uri 'self'"
            )
        else:
            response.headers["content-security-policy"] = "default-src 'self'; frame-ancestors 'none'; base-uri 'self'"
        response.headers["x-kingdom-ai-os-latency-ms"] = str(elapsed_ms)
        return response


__all__ = ["KingdomSecurityMiddleware"]
