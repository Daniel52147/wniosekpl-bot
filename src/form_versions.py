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
        helper_docs = {
            "umowa_najmu": {
                "ru": "📅 Szablon umowy — wersja pomocnicza WniosekPL",
                "en": "📅 Agreement template — helper version",
                "ua": "📅 Szablon umowy — wersja pomocnicza",
                "pl": "📅 Szablon umowy — wersja pomocnicza WniosekPL",
            },
            "pismo_do_urzedu": {
                "ru": "📅 Szablon pisma do urzędu — WniosekPL",
                "en": "📅 Office letter template — WniosekPL",
                "ua": "📅 Шаблон листа до urzędu — WniosekPL",
                "pl": "📅 Szablon pisma do urzędu — WniosekPL",
            },
            "upowaznienie": {
                "ru": "📅 Szablon upoważnienia — WniosekPL",
                "en": "📅 Authorization template — WniosekPL",
                "ua": "📅 Шаблон upoważnienia — WniosekPL",
                "pl": "📅 Szablon upoważnienia — WniosekPL",
            },
            "oswiadczenie_dochodow": {
                "ru": "📅 Szablon oświadczenia o dochodach — WniosekPL",
                "en": "📅 Income declaration template — WniosekPL",
                "ua": "📅 Шаблон заяви про доходи — WniosekPL",
                "pl": "📅 Szablon oświadczenia o dochodach — WniosekPL",
            },
        }
        if doc_id in helper_docs:
            return helper_docs[doc_id].get(lang, helper_docs[doc_id]["ru"])
        return ""

    code = entry.get("form_code", doc_id)
    labels = {
        "ru": f"📅 <b>Blanke aktualny na:</b> {FORM_CATALOG_DATE}\n<code>{code}</code>",
        "en": f"📅 <b>Form current as of:</b> {FORM_CATALOG_DATE}\n<code>{code}</code>",
        "ua": f"📅 <b>Бланк актуальний на:</b> {FORM_CATALOG_DATE}\n<code>{code}</code>",
        "pl": f"📅 <b>Formularz aktualny na:</b> {FORM_CATALOG_DATE}\n<code>{code}</code>",
    }
    return labels.get(lang, labels["ru"])
