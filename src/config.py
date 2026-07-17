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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_AI_MONTHLY = os.getenv("STRIPE_PRICE_AI_MONTHLY", "")
STRIPE_PRICE_HUMAN_REVIEW = os.getenv("STRIPE_PRICE_HUMAN_REVIEW", "")

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "")
SESSION_DAYS = int(os.getenv("SESSION_DAYS", "30"))
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_FROM = os.getenv("SMTP_FROM", "")
DEFAULT_COUNTRY = os.getenv("DEFAULT_COUNTRY", "pl").lower()


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
