"""Multi-country product surface. Poland is live; others are staged."""

from __future__ import annotations

COUNTRIES = [
    {
        "code": "pl",
        "name": "Poland",
        "status": "live",
        "currency": "PLN",
        "languages": ["pl", "ru", "ua", "en"],
        "focus": ["PESEL", "meldunek", "karta pobytu", "pisma do urzędu"],
    },
    {
        "code": "de",
        "name": "Germany",
        "status": "coming",
        "currency": "EUR",
        "languages": ["de", "en", "ru", "ua"],
        "focus": ["Anmeldung", "Aufenthaltstitel", "Jobcenter basics"],
    },
    {
        "code": "cz",
        "name": "Czechia",
        "status": "coming",
        "currency": "CZK",
        "languages": ["cs", "en", "ru", "ua"],
        "focus": ["trvalý pobyt", "registrace", "pracovní povolení"],
    },
    {
        "code": "lt",
        "name": "Lithuania",
        "status": "research",
        "currency": "EUR",
        "languages": ["lt", "en", "ru", "ua"],
        "focus": ["migracija", "leidimas gyventi"],
    },
]


def list_countries(status: str | None = None) -> list[dict]:
    items = COUNTRIES
    if status:
        items = [c for c in items if c["status"] == status]
    return items


def get_country(code: str) -> dict | None:
    code = (code or "").lower()
    for item in COUNTRIES:
        if item["code"] == code:
            return item
    return None


def active_country_code() -> str:
    return "pl"
