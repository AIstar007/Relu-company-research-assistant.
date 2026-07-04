<div align="center">

# 🔍 Relu Company Research Assistant

### AI-Powered · Web-Crawling · PDF Reports · Discord Delivery

[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js_14-Frontend-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Any_LLM-6C47FF?style=for-the-badge&logo=openai&logoColor=white)](https://openrouter.ai/)
[![Serper](https://img.shields.io/badge/Serper.dev-Web_Search-FF6B35?style=for-the-badge&logo=google&logoColor=white)](https://serper.dev/)
[![WeasyPrint](https://img.shields.io/badge/WeasyPrint-PDF_Reports-E74C3C?style=for-the-badge&logo=adobeacrobatreader&logoColor=white)](https://weasyprint.org/)
[![Discord](https://img.shields.io/badge/Discord-Auto_Delivery-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.com/)

<br/>

> **Drop in a company name or URL. Get a full AI research report — in seconds.**  
> Crawls the web · Enriches with search · Analyzes with AI · Exports to PDF · Delivers via Discord.

<br/>

[🚀 Quick Start](#-quick-start) · [🏗️ Architecture](#️-architecture) · [🔄 Request Flow](#-request-flow) · [⚙️ Configuration](#️-configuration) · [🚢 Deployment](#-deployment) · [🎨 Design Choices](#-design-choices)

---

</div>

## ✨ What It Does

Give it **any company name or website URL** and it:

| Step | Action |
|---|---|
| 🌐 **Resolves** | Finds the official website via Serper.dev (filters aggregators like LinkedIn/Wikipedia) |
| 🕷️ **Crawls** | Discovers & scores internal links, fetches top pages concurrently, strips boilerplate |
| 🔎 **Enriches** | Secondary search pass for phone/address data not always on-site |
| 🤖 **Analyzes** | OpenRouter LLM generates summary, products/services, pain points, industry label |
| 🏆 **Ranks Competitors** | Second LLM call deduplicates and ranks competitor candidates |
| 📄 **Exports PDF** | WeasyPrint renders a professionally styled, downloadable report |
| 💬 **Delivers (optional)** | Sends PDF + applicant info to your Discord channel via Bot API |

All through a **dark, ChatGPT-style chat interface** — no database, no auth, zero persisted state.

---

## 🏗️ Architecture

```
relu-research-assistant/
│
├── 📁 backend/                     FastAPI service
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   └── schemas.py
│   ├── services/
│   │   ├── search.py               Serper.dev — website resolution, competitors, contacts
│   │   ├── crawler.py              Site discovery + crawling + content extraction
│   │   ├── ai_engine.py            OpenRouter — structured analysis + competitor ranking
│   │   ├── pdf_generator.py        WeasyPrint HTML → PDF report builder
│   │   └── discord_bot.py          Discord Bot API — report + applicant delivery
│   └── routers/
│       ├── research.py             POST /api/research — full orchestration pipeline
│       └── discord.py              POST /api/discord/test — validate bot token/channel
│
└── 📁 frontend/                    Next.js 14 (App Router) + Tailwind
    ├── app/page.tsx                 Chat interface, examples, progress states
    ├── components/Sidebar.tsx       API keys + Discord config tabs
    ├── components/ResearchCard.tsx  Rendered research result + PDF download
    └── lib/api.ts                   Backend client
```

---

## 🔄 Request Flow

```
User Input (company name or URL)
        │
        ▼
┌───────────────────┐
│  1. RESOLVE       │  Serper.dev → find official website URL
│  (if not URL)     │  Filter: Wikipedia, LinkedIn, aggregators blocked
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  2. CRAWL         │  Fetch homepage → discover internal links
│                   │  Score by keyword relevance (about/products/pricing…)
│                   │  Top pages fetched concurrently → strip nav/footer/scripts
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  3. ENRICH        │  Secondary Serper pass → phone, address, contact hints
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  4. ANALYZE       │  All crawled text → OpenRouter (user-chosen model)
│                   │  JSON-only prompt → summary, products, pain points, industry
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  5. COMPETITORS   │  Serper finds candidates → second LLM call ranks them
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  6. PDF           │  WeasyPrint renders HTML/CSS → base64 PDF returned
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  7. DISCORD       │  (Optional) PDF + applicant info → Discord Bot API
│  (if configured)  │
└───────────────────┘
```

---

## 🚀 Quick Start

### Backend

```bash
cd backend
python -m venv venv

# Activate
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows

pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

> **WeasyPrint system dependencies** (required for PDF generation):
>
> ```bash
> # macOS
> brew install pango gdk-pixbuf libffi
>
> # Ubuntu / Debian
> apt-get install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev libcairo2
> ```
>
> 🐳 Using Docker? The included `Dockerfile` handles all of this automatically.

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local        # Set NEXT_PUBLIC_API_URL to your backend URL
npm run dev
```

Visit `http://localhost:3000` — the ChatGPT-style interface will be live.

---

## ⚙️ Configuration

### Environment Variables

| Location | Variable | Required | Description |
|---|---|---|---|
| Frontend | `NEXT_PUBLIC_API_URL` | ✅ Yes | Base URL of FastAPI backend — no trailing slash |
| Backend | *(none)* | — | All keys are entered in-app, not stored server-side |

### In-App Configuration (Sidebar)

Entered by the user per session, never persisted to disk or database:

| Setting | Description |
|---|---|
| 🤖 **OpenRouter API Key** | Your OpenRouter key |
| 🧠 **Model Selection** | Any OpenRouter model string (default: `openai/gpt-4o-mini`) |
| 🔎 **Serper.dev API Key** | Powers website resolution + competitor search |
| 💬 **Discord Bot Token** | Optional — for auto-delivery |
| 📢 **Discord Channel ID** | Optional — target channel for report delivery |
| 👤 **Applicant Name + Email** | Optional — included in Discord submission |

---

## 🚢 Deployment

### Frontend → Vercel

```bash
# Set environment variable in Vercel dashboard:
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

### Backend → Railway / Render / Fly.io

```bash
# Build and run with Docker (recommended)
docker build -t relu-backend ./backend
docker run -p 8000:8000 relu-backend
```

> ⚠️ **Avoid pure serverless functions** — crawling + multiple sequential AI calls can exceed short function timeouts. Use a persistent container service.

---

## 🎨 Design Choices

| Decision | Rationale |
|---|---|
| **`httpx` + BeautifulSoup** over headless browser | Fast, dependency-light; sufficient for server-rendered marketing pages |
| **WeasyPrint** (HTML/CSS → PDF) | Report layout stays easy to iterate; matches required visual spec closely |
| **User-controlled model** | Any OpenRouter model string works; nothing hardcoded beyond a sensible default |
| **No persistence** | Every request is fully stateless; API keys never touch a DB or disk — by design |
| **Page cap: 8 pages / 6000 chars** | Keeps AI prompt size bounded and costs predictable |

---

## 🛡️ API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/research` | Full orchestration pipeline — crawl → analyze → PDF |
| `POST` | `/api/discord/test` | Validate Discord bot token and channel ID |

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Frontend | [Next.js 14](https://nextjs.org/) + [Tailwind CSS](https://tailwindcss.com/) |
| LLM Provider | [OpenRouter](https://openrouter.ai/) (any model) |
| Web Search | [Serper.dev](https://serper.dev/) |
| Web Crawling | [httpx](https://www.python-httpx.org/) + [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) |
| PDF Generation | [WeasyPrint](https://weasyprint.org/) |
| Discord Delivery | [Discord Bot API](https://discord.com/developers/docs/intro) |
| Containerization | Docker |

---

## Note

This Assistant cannot scrap every websites because of the security policies differ company to company

### Use Case Relevation

Amazon is one of the most aggressively bot-protected sites on the internet (Akamai/PerimeterX-style bot detection, JS-rendered content, region-redirects, sometimes CAPTCHA challenges). Your crawler uses plain httpx (no headless browser), so when it hits Amazon, one of these happens:

Amazon detects it's not a real browser and returns a bot-check/redirect page instead of the real homepage
The real content is loaded via JavaScript after page load, which httpx never executes — it only sees the raw initial HTML, which is often empty or boilerplate
After stripping nav/footer/script (as your extract_clean_text does), there's nothing meaningful left → crawl_site returns an empty dict → your explicit check if not crawled_pages: raise HTTPException(...) fires

This is actually the correct, honest behavior for a scraping-based tool — meta and telegram work because their marketing pages are simpler/less protected.

---

<div align="center">

Built with ❤️ for AI-powered research automation

[⭐ Star this repo](#) · [🐛 Report an Issue](#) · [💡 Request a Feature](#)

</div>
