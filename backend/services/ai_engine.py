"""
OpenRouter integration. The user picks any OpenRouter-supported model string
(e.g. "openai/gpt-4o-mini", "anthropic/claude-3.5-sonnet", "google/gemini-2.0-flash-001")
and it's passed straight through — no hardcoded model.
"""
import json
import re
from typing import Dict, List, Any

import httpx

from config import OPENROUTER_BASE_URL, REQUEST_TIMEOUT_SECONDS

ANALYSIS_SYSTEM_PROMPT = """You are a B2B company research analyst. You will be given \
raw crawled text from a company's website plus optional public-search snippets. \
Respond with ONLY a single valid JSON object (no markdown fences, no preamble, no \
commentary) matching exactly this schema:

{
  "name": "string - the company's official/display name",
  "phone": "string or null",
  "address": "string or null - HQ or primary office address if mentioned",
  "products_services": ["array of short strings, 3-8 items"],
  "pain_points": ["array of 3-6 strings - realistic business pain points this company \
likely faces, inferred from their market position, product complexity, and industry"],
  "summary": "string - 2-3 sentence company overview",
  "industry": "string - short industry/category label used later for competitor search"
}

Be specific and grounded in the provided text. If a field truly cannot be determined, \
use null (for phone/address) or a best-effort inference (for the others). Never \
fabricate a phone number or address that isn't implied by the source text."""

COMPETITOR_SYSTEM_PROMPT = """You are a market research analyst. Given a target company \
and a list of raw web-search snippets, identify real, distinct competitor companies \
(same industry, same country if determinable, similar products/services). Respond with \
ONLY a valid JSON array (no markdown fences, no commentary), max 6 items, schema:

[{"name": "string", "website": "string or null - homepage URL only"}]

Exclude the target company itself, aggregator sites (review sites, wikis, social \
networks), and duplicates."""


def _strip_json_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


async def _call_openrouter(system_prompt: str, user_content: str, api_key: str, model: str) -> str:
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        resp = await client.post(
            OPENROUTER_BASE_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://relu-research-assistant.example",
                "X-Title": "Relu Company Research Assistant",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                ],
                "temperature": 0.3,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]


async def analyze_company(
    crawled_pages: Dict[str, str],
    contact_snippets: str,
    company_name_hint: str,
    api_key: str,
    model: str,
) -> Dict[str, Any]:
    pages_blob = "\n\n---\n\n".join(f"PAGE: {url}\n{text}" for url, text in crawled_pages.items())
    user_content = (
        f"Target company (from user query / resolved website): {company_name_hint}\n\n"
        f"CRAWLED WEBSITE CONTENT:\n{pages_blob[:18000]}\n\n"
        f"ADDITIONAL PUBLIC SEARCH SNIPPETS (may contain phone/address):\n{contact_snippets[:2000]}"
    )
    raw = await _call_openrouter(ANALYSIS_SYSTEM_PROMPT, user_content, api_key, model)
    cleaned = _strip_json_fences(raw)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError(f"AI response was not valid JSON: {raw[:300]}")


async def rank_competitors(
    company_name: str,
    industry: str,
    candidates: List[Dict[str, str]],
    api_key: str,
    model: str,
) -> List[Dict[str, str]]:
    if not candidates:
        return []
    candidates_blob = "\n".join(
        f"- {c['title']} | {c['link']} | {c['snippet']}" for c in candidates
    )
    user_content = (
        f"Target company: {company_name}\nIndustry: {industry}\n\n"
        f"Raw search results to evaluate:\n{candidates_blob}"
    )
    raw = await _call_openrouter(COMPETITOR_SYSTEM_PROMPT, user_content, api_key, model)
    cleaned = _strip_json_fences(raw)
    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\[.*\]", cleaned, re.DOTALL)
        result = json.loads(match.group(0)) if match else []
    return result if isinstance(result, list) else []
