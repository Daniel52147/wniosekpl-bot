import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = ROOT / "documents"
OUTPUT_DIR = ROOT / "data" / "generated"
UPLOADS_DIR = ROOT / "data" / "uploads"
KNOWLEDGE_DIR = ROOT / "knowledge"

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_USERNAME = os.getenv("BOT_USERNAME", "wniosekpl_bot")
FREE_MODE = os.getenv("FREE_MODE", "true").lower() in ("1", "true", "yes")
RELAX_SSL = os.getenv("RELAX_SSL", "false").lower() in ("1", "true", "yes")
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", str(ROOT / "data" / "urzad.db")))
DATABASE_URL = os.getenv("DATABASE_URL", "").strip()
AI_FREE_DAILY_LIMIT = int(os.getenv("AI_FREE_DAILY_LIMIT", "5"))
WEB_CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("WEB_CORS_ORIGINS", "*").split(",")
    if origin.strip()
]

PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

# OmniRoute gateway (https://github.com/diegosouzapw/OmniRoute)
# Default: OpenAI-compatible /v1 on local OmniRoute.
OMNIROUTE_ENABLED = os.getenv("OMNIROUTE_ENABLED", "true").lower() in (
    "1",
    "true",
    "yes",
)
OMNIROUTE_BASE_URL = os.getenv(
    "OMNIROUTE_BASE_URL",
    "http://127.0.0.1:20128/v1",
).rstrip("/")
OMNIROUTE_API_KEY = os.getenv("OMNIROUTE_API_KEY", "")
OMNIROUTE_MODEL = os.getenv("OMNIROUTE_MODEL", "auto")

# Direct OpenAI / OpenAI-compatible (used if OmniRoute off or as fallback)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Extra free/cheap provider keys (OmniRoute-style cascade without the gateway)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
LLM_FALLBACK_MODELS = {
    "groq": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
    "openrouter": os.getenv("OPENROUTER_MODEL", "openrouter/free"),
}

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_AI_MONTHLY = os.getenv("STRIPE_PRICE_AI_MONTHLY", "")
STRIPE_PRICE_HUMAN_REVIEW = os.getenv("STRIPE_PRICE_HUMAN_REVIEW", "")

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "")
APP_SECRET = os.getenv("APP_SECRET", "") or ADMIN_API_KEY or "wniosekpl-dev-secret-change-me"
SESSION_DAYS = int(os.getenv("SESSION_DAYS", "30"))
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_FROM = os.getenv("SMTP_FROM", "")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "pl").lower()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")
FACEBOOK_APP_ID = os.getenv("FACEBOOK_APP_ID", "")
FACEBOOK_APP_SECRET = os.getenv("FACEBOOK_APP_SECRET", "")


def database_backend() -> str:
    url = (DATABASE_URL or "").lower()
    if url.startswith("postgres"):
        return "postgres"
    return "sqlite"

_raw_admins = os.getenv("ADMIN_TELEGRAM_IDS", "")
ADMIN_IDS: set[int] = {
    int(x.strip()) for x in _raw_admins.split(",") if x.strip().isdigit()
}

PLAN_PRICES = {
    "ai_subscription": {"amount_pln": 19, "label": "AI unlimited / month"},
    "human_review": {"amount_pln": 29, "label": "Human document review"},
}

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
