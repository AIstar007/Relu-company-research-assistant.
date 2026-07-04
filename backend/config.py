"""
App-wide constants. No secrets live here — API keys (OpenRouter, Serper,
Discord) are supplied per-request from the frontend and are never persisted,
per the assignment's "no auth / no database" requirement.
"""

CRAWL_PAGE_LIMIT = 8
CRAWL_TIMEOUT_SECONDS = 10
REQUEST_TIMEOUT_SECONDS = 30

# Keyword hints used to prioritize which discovered links get crawled.
PRIORITY_PATH_KEYWORDS = [
    "about", "product", "service", "solution",
    "contact", "pricing", "plans", "company", "team",
]

# Paths that should never be crawled.
IGNORED_PATH_KEYWORDS = [
    "login", "signin", "sign-in", "signup", "sign-up", "register",
    "account", "cart", "checkout", "privacy", "terms", "cookie",
    "careers/apply", "wp-admin", "wp-login",
]

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; ReluResearchBot/1.0; "
        "+https://relu-consultancy.example/bot)"
    )
}

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
SERPER_SEARCH_URL = "https://google.serper.dev/search"
DISCORD_API_BASE = "https://discord.com/api/v10"
