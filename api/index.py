"""Vercel Python Serverless Entrypoint -> Exports Pure FastAPI `app`."""

from backend.main import app

__all__ = ["app"]
