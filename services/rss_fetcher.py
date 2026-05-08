"""
services/rss_fetcher.py
Mengambil dan memfilter berita dari RSS feed
"""
import feedparser
import asyncio
import aiohttp
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
from config.settings import KLUB_EROPA

logger = logging.getLogger(__name__)

# Batas waktu: hanya ambil berita dalam 24 jam terakhir
HOURS_LIMIT = 24


def _is_recent(entry) -> bool:
    """Cek apakah berita dalam rentang 24 jam terakhir."""
    try:
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            pub_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            cutoff = datetime.now(timezone.utc) - timedelta(hours=HOURS_LIMIT)
            return pub_dt >= cutoff
    except Exception:
        pass
    return True  # Default: anggap baru jika tidak ada info waktu


def _clean_summary(text: str, max_len: int = 200) -> str:
    """Bersihkan dan potong ringkasan berita."""
    if not text:
        return ""
    # Hapus tag HTML sederhana
    import re
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&#39;", "'").replace("&nbsp;", " ")
    text = " ".join(text.split())
    if len(text) > max_len:
        text = text[:max_len].rsplit(" ", 1)[0] + "..."
    return text


def _parse_feed(url: str) -> List[Dict]:
    """Parse satu RSS feed secara sinkron."""
    try:
        feed = feedparser.parse(url)
        results = []
        for entry in feed.entries:
            if not _is_recent(entry):
                continue
            item = {
                "title": entry.get("title", "").strip(),
                "link":  entry.get("link", ""),
                "summary": _clean_summary(
                    entry.get("summary", entry.get("description", ""))
                ),
                "source": feed.feed.get("title", url),
                "published": entry.get("published", ""),
            }
            if item["title"] and item["link"]:
                results.append(item)
        return results
    except Exception as e:
        logger.warning(f"Gagal parse feed {url}: {e}")
        return []


async def fetch_feeds_async(urls: List[str]) -> List[Dict]:
    """Ambil banyak feed secara async untuk kecepatan."""
    loop = asyncio.get_event_loop()
    tasks = [
        loop.run_in_executor(None, _parse_feed, url)
        for url in urls
    ]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    all_items = []
    for r in results:
        if isinstance(r, list):
            all_items.extend(r)
    # Hapus duplikat berdasarkan judul
    seen_titles = set()
    unique = []
    for item in all_items:
        key = item["title"].lower()[:60]
        if key not in seen_titles:
            seen_titles.add(key)
            unique.append(item)
    return unique


async def get_geopolitik_news(max_items: int = 5) -> List[Dict]:
    """Ambil berita geopolitik."""
    from config.settings import FEEDS_GEOPOLITIK
    news = await fetch_feeds_async(FEEDS_GEOPOLITIK)
    return news[:max_items]


async def get_financial_global_news(max_items: int = 5) -> List[Dict]:
    """Ambil berita keuangan global."""
    from config.settings import FEEDS_FINANCIAL_GLOBAL
    news = await fetch_feeds_async(FEEDS_FINANCIAL_GLOBAL)
    return news[:max_items]


async def get_financial_indonesia_news(max_items: int = 5) -> List[Dict]:
    """Ambil berita keuangan Indonesia."""
    from config.settings import FEEDS_FINANCIAL_INDONESIA
    news = await fetch_feeds_async(FEEDS_FINANCIAL_INDONESIA)
    return news[:max_items]


async def get_bola_eropa_news(max_items: int = 6) -> List[Dict]:
    """Ambil berita bola, filter yang berkaitan dengan klub Eropa."""
    from config.settings import FEEDS_BOLA_EROPA
    all_news = await fetch_feeds_async(FEEDS_BOLA_EROPA)

    # Filter berita yang menyebut klub Eropa
    klub_lower = [k.lower() for k in KLUB_EROPA]
    filtered = []
    for item in all_news:
        text = (item["title"] + " " + item["summary"]).lower()
        if any(k in text for k in klub_lower):
            filtered.append(item)

    # Jika filter terlalu ketat, ambil semua berita bola
    if len(filtered) < 3:
        filtered = all_news

    return filtered[:max_items]
