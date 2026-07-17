"""Lawyer / specialist marketplace (lead funnel, not a booking engine yet)."""

from __future__ import annotations

LAWYERS = [
    {
        "id": "migracja_warszawa",
        "name": "Migracja Desk Warszawa",
        "city": "Warszawa",
        "languages": ["pl", "ru", "ua", "en"],
        "specialties": ["karta pobytu", "odwołanie", "zezwolenie na pracę"],
        "price_from_pln": 350,
        "remote": True,
        "bio": "Pomoc w sprawach cudzoziemców i kompletowaniu dokumentów do UW.",
    },
    {
        "id": "pobyt_krakow",
        "name": "Pobyt Legal Kraków",
        "city": "Kraków",
        "languages": ["pl", "en", "ua"],
        "specialties": ["karta pobytu", "studia", "rodzina"],
        "price_from_pln": 300,
        "remote": True,
        "bio": "Checklisty i reprezentacja w Małopolsce.",
    },
    {
        "id": "zus_tax_remote",
        "name": "ZUS & Tax Remote",
        "city": "Polska",
        "languages": ["pl", "ru", "en"],
        "specialties": ["ZUS", "PIT", "umowa o pracę"],
        "price_from_pln": 200,
        "remote": True,
        "bio": "Konsultacje zdalne: ubezpieczenia i podstawy rozliczeń.",
    },
    {
        "id": "odwolania_desk",
        "name": "Odwołania Desk",
        "city": "Warszawa",
        "languages": ["pl", "ru", "en"],
        "specialties": ["odmowa", "wezwanie", "odwołanie"],
        "price_from_pln": 450,
        "remote": True,
        "bio": "Analiza decyzji i przygotowanie odpowiedzi / odwołania.",
    },
    {
        "id": "student_help_poznan",
        "name": "Student Stay Poznań",
        "city": "Poznań",
        "languages": ["pl", "en", "ua"],
        "specialties": ["studia", "karta pobytu", "ubezpieczenie"],
        "price_from_pln": 250,
        "remote": True,
        "bio": "Pakiet dokumentów dla studentów i umów najmu.",
    },
    {
        "id": "trojmiasto_migracja",
        "name": "Trójmiasto Migracja",
        "city": "Gdańsk",
        "languages": ["pl", "ru", "ua", "en"],
        "specialties": ["karta pobytu", "praca", "rodzina"],
        "price_from_pln": 320,
        "remote": True,
        "bio": "Pomoc w Gdańsku / Gdyni / Sopocie + zdalnie.",
    },
]


def list_lawyers(
    *,
    city: str | None = None,
    specialty: str | None = None,
    language: str | None = None,
) -> list[dict]:
    items = LAWYERS
    if city:
        c = city.lower()
        items = [x for x in items if c in x["city"].lower() or x["city"] == "Polska"]
    if specialty:
        s = specialty.lower()
        items = [x for x in items if any(s in t.lower() for t in x["specialties"])]
    if language:
        lang = language.lower()
        items = [x for x in items if lang in x["languages"]]
    return items


def get_lawyer(lawyer_id: str) -> dict | None:
    for item in LAWYERS:
        if item["id"] == lawyer_id:
            return item
    return None
