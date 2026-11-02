"""Router for Web/Scraping (web_scraping)."""
from __future__ import annotations

from backend.api.routers import make_tab_router

router = make_tab_router(
    "web_scraping",
    "Web/Scraping",
    "Scraping with Apify, Scrapy, Playwright, Selenium, queue fairness, robots policy, and schema extraction.",
)

__all__ = ["router"]
