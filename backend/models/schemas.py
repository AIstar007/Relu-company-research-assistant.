from typing import List, Optional
from pydantic import BaseModel, Field


class ApiKeys(BaseModel):
    """Keys are supplied by the client on every request; nothing is stored server-side."""
    openrouter_api_key: str
    serper_api_key: str
    ai_model: str = Field(default="openai/gpt-4o-mini")


class DiscordConfig(BaseModel):
    bot_token: Optional[str] = None
    channel_id: Optional[str] = None
    applicant_name: Optional[str] = None
    applicant_email: Optional[str] = None


class ResearchRequest(BaseModel):
    query: str  # company name OR website URL
    keys: ApiKeys
    discord: Optional[DiscordConfig] = None


class Competitor(BaseModel):
    name: str
    website: Optional[str] = None


class CompanyInfo(BaseModel):
    name: str
    website: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    products_services: List[str] = []
    pain_points: List[str] = []
    summary: Optional[str] = None


class ResearchResponse(BaseModel):
    company: CompanyInfo
    competitors: List[Competitor] = []
    pdf_base64: str
    sent_to_discord: bool = False
    sources_crawled: List[str] = []


class ProgressEvent(BaseModel):
    stage: str
    message: str
    done: bool = False
