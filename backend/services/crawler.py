"""
Lightweight async site crawler.

Strategy:
1. Fetch the homepage.
2. Parse all internal <a> links.
3. Score links by keyword match against PRIORITY_PATH_KEYWORDS.
4. Drop duplicates (by normalized path) and anything matching IGNORED_PATH_KEYWORDS.
5. Fetch the top N pages concurrently and extract clean text from each.

No headless browser — most marketing/company sites are server-rendered enough
for httpx + BeautifulSoup to get meaningful content, which keeps this fast
and dependency-light for a 6-hour build.
"""
import asyncio
from typing import List, Dict
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

from config import (
    CRAWL_PAGE_LIMIT,
    CRAWL_TIMEOUT_SECONDS,
    DEFAULT_HEADERS,
    PRIORITY_PATH_KEYWORDS,
    IGNORED_PATH_KEYWORDS,
)


def _normalize_path(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/") or "/"
    return f"{parsed.netloc.lower()}{path.lower()}"


def _is_ignored(url: str) -> bool:
    low = url.lower()
    return any(kw in low for kw in IGNORED_PATH_KEYWORDS)


def _priority_score(url: str) -> int:
    low = url.lower()
    for i, kw in enumerate(PRIORITY_PATH_KEYWORDS):
        if kw in low:
            return len(PRIORITY_PATH_KEYWORDS) - i
    return 0


async def _fetch(client: httpx.AsyncClient, url: str) -> str:
    try:
        resp = await client.get(url, headers=DEFAULT_HEADERS, follow_redirects=True, timeout=CRAWL_TIMEOUT_SECONDS)
        resp.raise_for_status()
        return resp.text
    except Exception:
        return ""


async def discover_pages(base_url: str) -> List[str]:
    """Return a de-duplicated, priority-ordered list of internal page URLs (including homepage)."""
    parsed_base = urlparse(base_url)
    root_netloc = parsed_base.netloc.lower()

    async with httpx.AsyncClient() as client:
        html = await _fetch(client, base_url)

    if not html:
        return [base_url]

    soup = BeautifulSoup(html, "lxml")
    seen_paths = {_normalize_path(base_url)}
    scored: List[tuple] = [(999, base_url)]  # homepage always first

    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)
        if parsed.netloc.lower() != root_netloc:
            continue  # external link, skip
        if _is_ignored(full_url):
            continue
        norm = _normalize_path(full_url)
        if norm in seen_paths:
            continue
        seen_paths.add(norm)
        scored.append((_priority_score(full_url), full_url.split("#")[0]))

    scored.sort(key=lambda x: x[0], reverse=True)
    ordered_urls = [u for _, u in scored]
    return ordered_urls[:CRAWL_PAGE_LIMIT]


def extract_clean_text(html: str, url: str) -> str:
    """Strip boilerplate (nav/footer/script/style) and return readable text."""
    if not html:
        return ""
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
        tag.decompose()
    for tag in soup.find_all(["nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator=" ", strip=True)
    text = " ".join(text.split())
    # Cap per-page length so the AI prompt doesn't blow up on huge pages.
    return text[:6000]


async def crawl_site(base_url: str) -> Dict[str, str]:
    """
    Discover priority pages and fetch+clean each one.
    Returns {url: clean_text} for successfully fetched pages.
    """
    pages = await discover_pages(base_url)

    async with httpx.AsyncClient() as client:
        htmls = await asyncio.gather(*[_fetch(client, url) for url in pages])

    result = {}
    for url, html in zip(pages, htmls):
        text = extract_clean_text(html, url)
        if text:
            result[url] = text
    return result
