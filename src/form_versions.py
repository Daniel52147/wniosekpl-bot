import json
from pathlib import Path

from src.config import ROOT

MANIFEST = ROOT / "templates" / "official" / "manifest.json"
FORM_CATALOG_DATE = "czerwiec 2025"


def _load() -> dict:
    if not MANIFEST.exists():
        return {}
    with MANIFEST.open(encoding="utf-8") as f:
        return json.load(f)


def version_line(doc_id: str, lang: str) -> str:
    entry = _load().get(doc_id)
    if not entry:
        if doc_id == "umowa_najmu":
            return {
                "ru": "📅 Szablon umowy — wersja pomocnicza WniosekPL",
                "en": "📅 Agreement template — helper version",
                "ua": "📅 Szablon umowy — wersja pomocnicza",
            }.get(lang, "")
        return ""

    code = entry.get("form_code", doc_id)
    labels = {
        "ru": f"📅 <b>Blanke aktualny na:</b> {FORM_CATALOG_DATE}\n<code>{code}</code>",
        "en": f"📅 <b>Form current as of:</b> {FORM_CATALOG_DATE}\n<code>{code}</code>",
        "ua": f"📅 <b>Бланк актуальний на:</b> {FORM_CATALOG_DATE}\n<code>{code}</code>",
        "pl": f"📅 <b>Formularz aktualny na:</b> {FORM_CATALOG_DATE}\n<code>{code}</code>",
    }
    return labels.get(lang, labels["ru"])
