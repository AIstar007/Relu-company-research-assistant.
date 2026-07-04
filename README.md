# Relu Company Research Assistant

AI-powered company research: give it a company name or website URL, it crawls
the site, enriches with public search (Serper.dev), runs AI analysis
(OpenRouter — any model you choose), identifies competitors, and generates a
downloadable, professionally styled PDF report — all through a ChatGPT-style
interface. Includes optional Discord auto-delivery of the report.

## Architecture

```
relu-research-assistant/
├── backend/            FastAPI service (crawling, search, AI, PDF, Discord)
│   ├── main.py
│   ├── config.py
│   ├── models/schemas.py
│   ├── services/
│   │   ├── search.py         Serper.dev: website resolution, competitor leads, contact info
│   │   ├── crawler.py        Site discovery + crawling + content extraction
│   │   ├── ai_engine.py      OpenRouter: structured company analysis + competitor ranking
│   │   ├── pdf_generator.py  WeasyPrint HTML->PDF report builder
│   │   └── discord_bot.py    Discord Bot API: sends report + applicant info
│   └── routers/
│       ├── research.py       POST /api/research — the full orchestration pipeline
│       └── discord.py        POST /api/discord/test — validate bot token/channel
└── frontend/            Next.js 14 (App Router) + Tailwind, dark ChatGPT-style UI
    ├── app/page.tsx           Chat interface, examples, progress states
    ├── components/Sidebar.tsx API keys + Discord config tabs
    ├── components/ResearchCard.tsx  Rendered research result + PDF download
    └── lib/api.ts              Backend client
```

### Request flow (`POST /api/research`)

1. **Resolve** — if the input isn't already a URL, Serper.dev finds the
   official website (aggregator domains like Wikipedia/LinkedIn are filtered out).
2. **Crawl** — the homepage is fetched, internal links are discovered and
   scored by keyword relevance (about/products/services/solutions/contact/pricing),
   deduplicated, and the top pages are fetched concurrently and cleaned of
   nav/footer/script boilerplate.
3. **Enrich** — a secondary Serper search grabs phone/address hints not
   always present on-site.
4. **Analyze** — all crawled text + hints go to OpenRouter (model chosen by
   the user) with a strict JSON-only prompt, returning company summary,
   products/services, AI-generated pain points, and an industry label.
5. **Competitors** — Serper searches for competitor candidates; a second
   OpenRouter call dedupes/ranks them into a clean name+website list.
6. **PDF** — WeasyPrint renders an HTML/CSS report matching the
   required layout and returns it as base64.
7. **Discord (optional)** — if configured, the PDF + applicant/company
   details are POSTed to the configured Discord channel via the Bot API.

No database, no authentication, no persisted state — all API keys are
supplied by the client per request and held only in browser memory for the
session, per the assignment's requirements.

## Setup

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

WeasyPrint needs a few system libraries for PDF rendering:
- **macOS:** `brew install pango gdk-pixbuf libffi`
- **Ubuntu/Debian:** `apt-get install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev libcairo2`
- The included `Dockerfile` already handles this for containerized deployment.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local   # set NEXT_PUBLIC_API_URL to your backend URL
npm run dev
```

Visit `http://localhost:3000`.

## Environment Variables

| Location | Variable | Required | Description |
|---|---|---|---|
| Frontend | `NEXT_PUBLIC_API_URL` | Yes | Base URL of the deployed FastAPI backend, no trailing slash |
| Backend | *(none)* | — | All external API keys are entered in the UI sidebar per session, not stored as backend env vars |

**In-app configuration (entered by the user, not env vars):**
- OpenRouter API key + model selection
- Serper.dev API key
- Discord Bot Token + Channel ID (bonus feature)
- Applicant name + email (for Discord submission)

## Deployment

- **Frontend:** Vercel — `NEXT_PUBLIC_API_URL` set to your backend's public URL.
- **Backend:** Railway, Render, or Fly.io (avoid pure serverless functions —
  crawling + multiple AI calls can exceed short function timeouts). The
  provided `backend/Dockerfile` builds a ready-to-deploy image with all
  WeasyPrint system dependencies included.

## Notes on design choices

- **Crawling** uses `httpx` + `BeautifulSoup` rather than a headless browser
  — fast and dependency-light, sufficient for the server-rendered marketing
  pages this use case targets. Pages are capped at 8 per site and 6000
  characters each to keep AI prompts bounded.
- **PDF generation** uses WeasyPrint (HTML/CSS → PDF) instead of a
  programmatic canvas API, so the report's visual styling stays easy to
  iterate on and matches the required layout closely.
- **Model choice** is fully user-controlled — any OpenRouter model string
  works, nothing is hardcoded beyond a sensible default (`openai/gpt-4o-mini`).
- **No persistence** — every request is stateless by design; API keys never
  touch a database or disk.
