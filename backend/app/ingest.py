from __future__ import annotations
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import feedparser
import requests
from bs4 import BeautifulSoup
from .storage import insert_live_item, log_refresh

KEYWORDS = ["hantavirus", "andes virus", "hps", "hantavirus pulmonary syndrome"]

FEEDS = [
    {
        "name": "WHO Disease Outbreak News",
        "url": "https://www.who.int/feeds/entity/csr/don/en/rss.xml",
    },
    {
        "name": "CDC Emerging Infectious Diseases",
        "url": "https://wwwnc.cdc.gov/eid/rss/current.xml",
    },
    {
        "name": "CDC Emerging Infectious Diseases - Ahead of Print",
        "url": "https://wwwnc.cdc.gov/eid/rss/ahead-of-print.xml",
    },
    {
        "name": "ECDC Latest News",
        "url": "https://www.ecdc.europa.eu/en/news-events/rss.xml",
    },
]

OFFICIAL_PAGES = [
    {
        "name": "CDC Andes Virus Situation Summary",
        "url": "https://www.cdc.gov/hantavirus/situation-summary/index.html",
    },
    {
        "name": "CDC Reported Hantavirus Cases",
        "url": "https://www.cdc.gov/hantavirus/data-research/cases/index.html",
    },
]


def _matches(text: str) -> list[str]:
    lowered = text.lower()
    return [kw for kw in KEYWORDS if kw in lowered]


def _clean_html(raw: str | None) -> str:
    if not raw:
        return ""
    soup = BeautifulSoup(raw, "html.parser")
    return re.sub(r"\s+", " ", soup.get_text(" ")).strip()


def _published(entry) -> str | None:
    for field in ["published", "updated", "created"]:
        value = entry.get(field)
        if value:
            try:
                return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
            except Exception:
                return value
    return None


def fetch_rss_items() -> list[dict]:
    items: list[dict] = []
    for feed in FEEDS:
        parsed = feedparser.parse(feed["url"])
        for entry in parsed.entries[:25]:
            title = _clean_html(entry.get("title", ""))
            summary = _clean_html(entry.get("summary", ""))
            text = f"{title} {summary}"
            matched = _matches(text)
            if not matched:
                continue
            items.append({
                "title": title,
                "source_name": feed["name"],
                "source_url": entry.get("link", feed["url"]),
                "published_at": _published(entry),
                "summary": summary[:900],
                "matched_keywords": matched,
            })
    return items


def fetch_official_pages() -> list[dict]:
    items: list[dict] = []
    headers = {"User-Agent": "HantaWatch educational tracker/1.0"}
    for page in OFFICIAL_PAGES:
        try:
            res = requests.get(page["url"], headers=headers, timeout=15)
            res.raise_for_status()
            soup = BeautifulSoup(res.text, "html.parser")
            title = soup.find("h1")
            title_text = title.get_text(" ", strip=True) if title else page["name"]
            body = soup.get_text(" ", strip=True)
            matched = _matches(body)
            if matched:
                items.append({
                    "title": title_text,
                    "source_name": page["name"],
                    "source_url": page["url"],
                    "published_at": datetime.now(timezone.utc).isoformat(),
                    "summary": body[:900],
                    "matched_keywords": matched,
                })
        except Exception:
            continue
    return items


def refresh_live_data() -> dict:
    try:
        items = fetch_rss_items() + fetch_official_pages()
        inserted = 0
        for item in items:
            if insert_live_item(item):
                inserted += 1
        log_refresh("success", len(items))
        return {"status": "success", "items_seen": len(items), "new_items": inserted}
    except Exception as exc:
        log_refresh("error", 0, str(exc))
        return {"status": "error", "items_seen": 0, "new_items": 0, "error": str(exc)}
