"""Check the RSS/Atom endpoints used by the GIX configuration."""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from pathlib import Path

import feedparser
import httpx

from src.scrapers.github import GitHubScraper
from src.scrapers.google_news import GoogleNewsScraper
from src.scrapers.hackernews import HackerNewsScraper
from src.storage.manager import StorageManager


async def check_feed(client: httpx.AsyncClient, name: str, url: str) -> tuple[str, str]:
    try:
        response = await client.get(url, follow_redirects=True)
        response.raise_for_status()
        parsed = feedparser.parse(response.text)
        if not parsed.entries:
            detail = str(getattr(parsed, "bozo_exception", "no entries"))
            return name, f"WARN 0 entries ({detail})"
        return name, f"OK {response.status_code}, {len(parsed.entries)} entries"
    except Exception as exc:
        return name, f"ERROR {type(exc).__name__}: {exc}"


async def main() -> int:
    root = Path(__file__).resolve().parents[1]
    config = StorageManager(config_path=str(root / "data" / "config.github.json")).load_config()
    timeout = httpx.Timeout(20.0, connect=10.0)
    headers = {"User-Agent": "Horizon-GIX-Feed-Check/1.0"}
    async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
        checks = [
            check_feed(client, source.name, str(source.url))
            for source in config.sources.rss
            if source.enabled
        ]
        results = await asyncio.gather(*checks)
        since = datetime.now(timezone.utc) - timedelta(hours=24)
        google_items = await GoogleNewsScraper(config.sources.google_news, client).fetch(since)
        github_items = await GitHubScraper(config.sources.github, client).fetch(since)
        hackernews_items = await HackerNewsScraper(
            config.sources.hackernews, client
        ).fetch(since)

    failures = 0
    for name, result in results:
        print(f"{name}: {result}")
        if result.startswith("ERROR"):
            failures += 1
    print(f"Google News query: OK, {len(google_items)} recent items")
    print(f"GitHub release sources: OK, {len(github_items)} releases in the last 24 hours")
    print(f"Hacker News: OK, {len(hackernews_items)} qualifying recent items")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
