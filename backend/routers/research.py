from fastapi import APIRouter, HTTPException

from models.schemas import ResearchRequest, ResearchResponse, CompanyInfo, Competitor
from services.search import (
    is_valid_url,
    normalize_url,
    resolve_official_website,
    find_competitor_candidates,
    find_contact_details,
)
from services.crawler import crawl_site
from services.ai_engine import analyze_company, rank_competitors
from services.pdf_generator import generate_pdf_base64
from services.discord_bot import send_report_to_discord

router = APIRouter(prefix="/api", tags=["research"])


@router.post("/research", response_model=ResearchResponse)
async def research_company(payload: ResearchRequest):
    query = payload.query.strip()
    keys = payload.keys

    if not query:
        raise HTTPException(400, "Please provide a company name or website URL.")

    # 1. Resolve to an official website
    try:
        if is_valid_url(query):
            website = normalize_url(query)
        else:
            website = await resolve_official_website(query, keys.serper_api_key)
    except Exception as exc:
        raise HTTPException(422, f"Could not resolve a website for '{query}': {exc}")

    # 2. Crawl the site
    try:
        crawled_pages = await crawl_site(website)
    except Exception as exc:
        raise HTTPException(502, f"Crawling failed for {website}: {exc}")

    if not crawled_pages:
        raise HTTPException(502, f"No readable content found at {website}.")

    # 3. Extra public info (phone/address hints) via Serper
    try:
        contact_snippets = await find_contact_details(query, keys.serper_api_key)
    except Exception:
        contact_snippets = ""

    # 4. AI analysis -> structured company info
    try:
        analysis = await analyze_company(
            crawled_pages, contact_snippets, query, keys.openrouter_api_key, keys.ai_model
        )
    except Exception as exc:
        raise HTTPException(502, f"AI analysis failed: {exc}")

    company = CompanyInfo(
        name=analysis.get("name") or query,
        website=website,
        phone=analysis.get("phone"),
        address=analysis.get("address"),
        products_services=analysis.get("products_services", []),
        pain_points=analysis.get("pain_points", []),
        summary=analysis.get("summary"),
    )
    industry = analysis.get("industry", "")

    # 5. Competitor discovery: Serper candidates -> AI ranks/dedupes
    try:
        candidates = await find_competitor_candidates(company.name, industry, keys.serper_api_key)
        ranked = await rank_competitors(company.name, industry, candidates, keys.openrouter_api_key, keys.ai_model)
        competitors = [Competitor(name=c.get("name", "Unknown"), website=c.get("website")) for c in ranked]
    except Exception:
        competitors = []

    # 6. PDF report
    pdf_base64 = generate_pdf_base64(company, competitors)

    # 7. Discord bonus - fire and forget, never blocks the response
    sent_to_discord = False
    if payload.discord and payload.discord.bot_token and payload.discord.channel_id:
        try:
            sent_to_discord = await send_report_to_discord(payload.discord, company, pdf_base64)
        except Exception:
            sent_to_discord = False

    return ResearchResponse(
        company=company,
        competitors=competitors,
        pdf_base64=pdf_base64,
        sent_to_discord=sent_to_discord,
        sources_crawled=list(crawled_pages.keys()),
    )
