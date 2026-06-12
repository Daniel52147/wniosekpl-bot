import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
DOCUMENTS_DIR = ROOT / "documents"
OUTPUT_DIR = ROOT / "data" / "generated"

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
BOT_USERNAME = os.getenv("BOT_USERNAME", "wniosekpl_bot")
FREE_MODE = os.getenv("FREE_MODE", "true").lower() in ("1", "true", "yes")
RELAX_SSL = os.getenv("RELAX_SSL", "false").lower() in ("1", "true", "yes")
DATABASE_PATH = Path(os.getenv("DATABASE_PATH", str(ROOT / "data" / "urzad.db")))

_raw_admins = os.getenv("ADMIN_TELEGRAM_IDS", "")
ADMIN_IDS: set[int] = {
    int(x.strip()) for x in _raw_admins.split(",") if x.strip().isdigit()
}

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
