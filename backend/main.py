from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import research, discord

app = FastAPI(
    title="Relu Company Research Assistant API",
    description="AI-powered company research: crawling + Serper search + OpenRouter analysis + PDF + Discord.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your deployed frontend origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research.router)
app.include_router(discord.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}
