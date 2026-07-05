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

**🌐 Live app:** [relu-frontend-gamma.vercel.app](https://relu-frontend-gamma.vercel.app)

[🚀 Quick Start](#-quick-start) · [🏗️ Architecture](#️-architecture) · [🔄 Request Flow](#-request-flow) · [⚙️ Configuration](#️-configuration) · [🚢 Deployment](#-deployment) · [🎨 Design Choices](#-design-choices)

---

</div>

## 📸 Live Demo

<div align="center">

### Main Interface
<img src="screenshots/Screenshot 1.png" alt="Main interface" width="800" />

### Research result view
<img src="screenshots/Screenshot 2.png" alt="Research result" width="800" />
<img src="screenshots/Screenshot 3.png" alt="Research result" width="800" />
<img src="screenshots/Screenshot 4.png" alt="Research result" width="800" />

</div>

<table>
<tr>
<td width="50%">

**📄 Generated PDF Report**
<img src="screenshots/Screenshot-10.png" alt="Generated PDF Report" width="800" />

</td>
<td width="50%">

**💬 Discord Auto-Delivery**
<img src="screenshots/Screenshot 9.png" alt="Discord Delivery" width="800" />

</td>
</tr>
</table>

---

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
├── 📁 frontend/                    Next.js 14 (App Router) + Tailwind
│   ├── app/page.tsx                 Chat interface, examples, progress states
│   ├── components/Sidebar.tsx       API keys + Discord config tabs
│   ├── components/ResearchCard.tsx  Rendered research result + PDF download
│   └── lib/api.ts                   Backend client
│
└── 📁 screenshots/                 Demo images used in this README
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
> apt-get install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libffi-dev libcairo2
> ```
>
> 🐳 Using Docker? The included `Dockerfile` handles all of this automatically.
>
> ⚠️ **Note:** `requirements.txt` pins `pydyf==0.10.0` alongside `weasyprint==62.3`. Newer `pydyf` releases (0.11+) removed an internal method WeasyPrint 62.3 depends on, which breaks PDF generation with an `AttributeError`. Keep this pin unless you also upgrade WeasyPrint.

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

**Live deployment:**
- Frontend: [relu-frontend-gamma.vercel.app](https://relu-frontend-gamma.vercel.app) (Vercel)
- Backend: Render (Docker)

### Frontend → Vercel

```bash
# Set environment variable in Vercel dashboard:
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

Set **Root Directory** to `frontend` when importing the project, since this is a monorepo.

### Backend → Render / Railway / Fly.io

```bash
# Build and run with Docker (recommended)
docker build -t relu-backend ./backend
docker run -p 8000:8000 relu-backend
```

> ⚠️ **Avoid pure serverless functions** — crawling + multiple sequential AI calls can exceed short function timeouts. Use a persistent container service.
>
> ⚠️ **Free-tier cold starts:** Render's free tier spins down after ~15 minutes idle. The first request after inactivity may take 30–50s while the container wakes up.

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
| `GET` | `/api/health` | Health check |

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

## ⚠️ Known Limitation: Bot-Protected Sites

This assistant crawls with a plain HTTP client (`httpx`), not a headless browser — a deliberate tradeoff for speed and low resource use (see [Design Choices](#-design-choices)). Sites with aggressive bot protection (Akamai/PerimeterX-style detection, JS-rendered content, CAPTCHA challenges) — **Amazon being a prime example** — may return a bot-check page or empty content instead of the real homepage.

When that happens, the crawler correctly detects it found no usable content and returns a clean error:
```json
{"detail": "No readable content found at https://www.amazon.com."}
```
rather than silently failing or fabricating data. Companies with simpler, less-protected marketing sites (Meta, Telegram, Stripe, etc. — see screenshots above) work reliably.

<img src="screenshots/Screenshot-18.png" alt="Discord Delivery" width="800" />

---

<div align="center">

Built with ❤️ for AI-powered research automation

[⭐ Star this repo](https://github.com/AIstar007/Relu-company-research-assistant.) · [🐛 Report an Issue](https://github.com/AIstar007/Relu-company-research-assistant./issues)

</div>
