"""
Sends the generated PDF + applicant/research details to a Discord channel
using the Discord Bot HTTP API (bot token + channel ID, both supplied by
the evaluator via the frontend's Discord Integration settings — never
hardcoded here).
"""
import base64
import json
import httpx

from config import DISCORD_API_BASE, REQUEST_TIMEOUT_SECONDS
from models.schemas import DiscordConfig, CompanyInfo


async def send_report_to_discord(
    config: DiscordConfig,
    company: CompanyInfo,
    pdf_base64: str,
) -> bool:
    if not config.bot_token or not config.channel_id:
        return False

    content = (
        f"**New Research Submission**\n"
        f"Applicant: {config.applicant_name or 'N/A'} ({config.applicant_email or 'N/A'})\n"
        f"Company: {company.name}\n"
        f"Website: {company.website or 'N/A'}"
    )

    pdf_bytes = base64.b64decode(pdf_base64)
    filename = f"{(company.name or 'company').replace(' ', '_').lower()}-research-report.pdf"

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        resp = await client.post(
            f"{DISCORD_API_BASE}/channels/{config.channel_id}/messages",
            headers={"Authorization": f"Bot {config.bot_token}"},
            data={"payload_json": json.dumps({"content": content})},
            files={"file": (filename, pdf_bytes, "application/pdf")},
        )
        return resp.status_code in (200, 201)
