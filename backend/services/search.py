"""
Serper.dev integration.

Used for:
- resolving a company name to its official website
- gathering supporting public info (phone/address hints, news mentions)
- finding competitor candidates
"""
import re
from typing import List, Dict, Any
from urllib.parse import urlparse

import httpx
import tldextract

from config import SERPER_SEARCH_URL, REQUEST_TIMEOUT_SECONDS

# Domains that are never the "official site" even if they rank highly.
AGGREGATOR_BLOCKLIST = {
    "wikipedia.org", "linkedin.com", "facebook.com", "twitter.com", "x.com",
    "instagram.com", "youtube.com", "crunchbase.com", "glassdoor.com",
    "indeed.com", "bloomberg.com", "reuters.com", "g2.com", "capterra.com",
    "trustpilot.com", "yelp.com", "medium.com", "github.com",
}


async def serper_search(query: str, api_key: str, num: int = 10) -> Dict[str, Any]:
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        resp = await client.post(
            SERPER_SEARCH_URL,
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": query, "num": num},
        )
        resp.raise_for_status()
        return resp.json()


def _root_domain(url: str) -> str:
    ext = tldextract.extract(url)
    return f"{ext.domain}.{ext.suffix}".lower()


def is_valid_url(text: str) -> bool:
    try:
        parsed = urlparse(text if "://" in text else f"https://{text}")
        return bool(parsed.netloc) and "." in parsed.netloc
    except Exception:
        return False


def normalize_url(text: str) -> str:
    if "://" not in text:
        text = f"https://{text}"
    parsed = urlparse(text)
    return f"{parsed.scheme}://{parsed.netloc}"


async def resolve_official_website(company_name: str, api_key: str) -> str:
    """Given a company name, find its most likely official website via Serper."""
    data = await serper_search(f"{company_name} official website", api_key, num=10)
    organic = data.get("organic", [])

    for result in organic:
        link = result.get("link", "")
        if not link:
            continue
        domain = _root_domain(link)
        if domain in AGGREGATOR_BLOCKLIST:
            continue
        return normalize_url(link)

    # fallback: Serper's own knowledge graph often has a "website" field
    kg = data.get("knowledgeGraph", {})
    if kg.get("website"):
        return normalize_url(kg["website"])

    raise ValueError(f"Could not resolve an official website for '{company_name}'.")


async def find_competitor_candidates(company_name: str, industry_hint: str, api_key: str) -> List[Dict[str, str]]:
    """Search for competitor names + let AI layer resolve/rank them later."""
    query = f"top competitors and alternatives to {company_name} {industry_hint}".strip()
    data = await serper_search(query, api_key, num=10)

    candidates = []
    for result in data.get("organic", []):
        title = result.get("title", "")
        link = result.get("link", "")
        snippet = result.get("snippet", "")
        if link and _root_domain(link) not in AGGREGATOR_BLOCKLIST | {_root_domain(company_name)}:
            candidates.append({"title": title, "link": link, "snippet": snippet})
    return candidates


async def find_contact_details(company_name: str, api_key: str) -> str:
    """Grab a snippet blob that may contain phone/address if not found on-site."""
    data = await serper_search(f"{company_name} phone number address headquarters", api_key, num=5)
    snippets = [r.get("snippet", "") for r in data.get("organic", [])]
    return "\n".join(s for s in snippets if s)
