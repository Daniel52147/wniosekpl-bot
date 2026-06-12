import json
from typing import Any

from src.database import get_profile, save_profile

PROFILE_LABELS: dict[str, dict[str, str]] = {
    "imie": {"ru": "Имя", "en": "First name", "ua": "Ім'я", "pl": "Imię"},
    "nazwisko": {"ru": "Фамилия", "en": "Last name", "ua": "Прізвище", "pl": "Nazwisko"},
    "data_urodzenia": {"ru": "Дата рождения", "en": "Date of birth", "ua": "Дата народження", "pl": "Data urodzenia"},
    "miejsce_urodzenia": {"ru": "Место рождения", "en": "Place of birth", "ua": "Місце народження", "pl": "Miejsce urodzenia"},
    "obywatelstwo": {"ru": "Гражданство", "en": "Citizenship", "ua": "Громадянство", "pl": "Obywatelstwo"},
    "numer_paszportu": {"ru": "Паспорт", "en": "Passport", "ua": "Паспорт", "pl": "Paszport"},
    "adres_zamieszkania": {"ru": "Адрес", "en": "Address", "ua": "Адреса", "pl": "Adres"},
    "pesel": {"ru": "PESEL", "en": "PESEL", "ua": "PESEL", "pl": "PESEL"},
    "imie_ojca": {"ru": "Имя отца", "en": "Father's name", "ua": "Ім'я батька", "pl": "Imię ojca"},
    "imie_matki": {"ru": "Имя матери", "en": "Mother's name", "ua": "Ім'я матері", "pl": "Imię matki"},
    "podstawa_prawna": {"ru": "Podstawa prawna", "en": "Legal basis", "ua": "Podstawa prawna", "pl": "Podstawa prawna"},
    "wlasciciel_nieruchomosci": {"ru": "Właściciel", "en": "Landlord", "ua": "Власник", "pl": "Właściciel"},
    "wynajmujacy_adres": {"ru": "Адрес wynajmującego", "en": "Landlord address", "ua": "Адреса орендодавця", "pl": "Adres wynajmującego"},
    "data_zameldowania": {"ru": "Data zameldowania", "en": "Registration date", "ua": "Data zameldowania", "pl": "Data zameldowania"},
    "data_wjazdu": {"ru": "Дата въезда", "en": "Entry date", "ua": "Дата в'їзду", "pl": "Data wjazdu"},
}


def profile_label(key: str, lang: str) -> str:
    return PROFILE_LABELS.get(key, {}).get(lang, key)


PROFILE_KEYS = {
    "imie",
    "nazwisko",
    "data_urodzenia",
    "miejsce_urodzenia",
    "obywatelstwo",
    "numer_paszportu",
    "adres_zamieszkania",
    "pesel",
    "imie_ojca",
    "imie_matki",
    "podstawa_prawna",
    "wlasciciel_nieruchomosci",
    "wynajmujacy_adres",
    "data_zameldowania",
    "data_wjazdu",
}


def pick_profile_fields(answers: dict[str, str]) -> dict[str, str]:
    return {k: v for k, v in answers.items() if k in PROFILE_KEYS and v.strip()}


async def update_profile(telegram_id: int, answers: dict[str, str]) -> None:
    existing = await get_profile(telegram_id) or {}
    merged = {**existing, **pick_profile_fields(answers)}
    await save_profile(telegram_id, merged)


META_LAST_DOC = "__last_doc__"


async def load_profile_prefill(telegram_id: int) -> dict[str, str]:
    raw = await get_profile(telegram_id) or {}
    return {k: v for k, v in raw.items() if not k.startswith("__")}


async def save_last_document(telegram_id: int, doc_id: str) -> None:
    data = await get_profile(telegram_id) or {}
    data[META_LAST_DOC] = doc_id
    await save_profile(telegram_id, data)


async def clear_profile(telegram_id: int) -> None:
    data = await get_profile(telegram_id) or {}
    last = data.get(META_LAST_DOC)
    await save_profile(telegram_id, {META_LAST_DOC: last} if last else {})


async def set_profile_field(telegram_id: int, key: str, value: str) -> None:
    if key not in PROFILE_KEYS:
        return
    data = await get_profile(telegram_id) or {}
    if value.strip():
        data[key] = value.strip()
    else:
        data.pop(key, None)
    await save_profile(telegram_id, data)


async def get_last_document(telegram_id: int) -> str | None:
    data = await get_profile(telegram_id) or {}
    doc_id = data.get(META_LAST_DOC)
    return doc_id if doc_id in ("pesel", "meldunek", "meldunek_staly", "umowa_najmu") else None
