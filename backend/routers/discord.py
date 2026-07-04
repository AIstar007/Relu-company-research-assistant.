import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config import DISCORD_API_BASE, REQUEST_TIMEOUT_SECONDS

router = APIRouter(prefix="/api/discord", tags=["discord"])


class DiscordTestRequest(BaseModel):
    bot_token: str
    channel_id: str


@router.post("/test")
async def test_discord_config(payload: DiscordTestRequest):
    """Lightweight check that the bot token + channel ID are valid before saving."""
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
        resp = await client.get(
            f"{DISCORD_API_BASE}/channels/{payload.channel_id}",
            headers={"Authorization": f"Bot {payload.bot_token}"},
        )
    if resp.status_code != 200:
        raise HTTPException(400, "Could not verify bot token / channel ID.")
    return {"ok": True, "channel": resp.json().get("name")}
