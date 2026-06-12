import re
from datetime import datetime

DATE_RE = re.compile(r"^\d{2}\.\d{2}\.\d{4}$")
PESEL_RE = re.compile(r"^\d{11}$")
POSTAL_RE = re.compile(r"\d{2}-\d{3}")
MONEY_RE = re.compile(r"^\d+([.,]\d{1,2})?$")

DATE_FIELDS = {
    "data_urodzenia",
    "data_wjazdu",
    "data_zameldowania",
    "data_rozpoczecia",
    "data_zakonczenia",
    "data_umowy",
    "data_od",
    "data_do",
}
MONEY_FIELDS = {"czynsz", "kaucja"}
PESEL_SKIP = {"brak", "nie", "\u043d\u0435\u0442", "no", "n/a", "-"}
OPTIONAL_FIELDS = {
    "imie_ojca",
    "imie_matki",
    "media_opis",
    "kaucja",
    "pesel",
    "data_do",
}


def _msg(key: str, lang: str) -> str:
    msgs = {
        "date": {
            "ru": "\u0424\u043e\u0440\u043c\u0430\u0442 \u0434\u0430\u0442\u044b: DD.MM.RRRR (\u043d\u0430\u043f\u0440. 15.03.1990)",
            "en": "Date format: DD.MM.RRRR (e.g. 15.03.1990)",
            "ua": "\u0424\u043e\u0440\u043c\u0430\u0442 \u0434\u0430\u0442\u0438: DD.MM.RRRR (\u043d\u0430\u043f\u0440. 15.03.1990)",
            "pl": "Format daty: DD.MM.RRRR (np. 15.03.1990)",
        },
        "pesel": {
            "ru": "PESEL \u2014 11 \u0446\u0438\u0444\u0440 \u0438\u043b\u0438 \u043d\u0430\u043f\u0438\u0448\u0438\u0442\u0435: brak",
            "en": "PESEL: 11 digits or type: brak",
            "ua": "PESEL \u2014 11 \u0446\u0438\u0444\u0440 \u0430\u0431\u043e: brak",
            "pl": "PESEL: 11 cyfr lub wpisz: brak",
        },
        "postal": {
            "ru": "\u0412 \u0430\u0434\u0440\u0435\u0441\u0435 \u043d\u0443\u0436\u0435\u043d \u0438\u043d\u0434\u0435\u043c: 00-000",
            "en": "Address needs postal code: 00-000",
            "ua": "\u0412 \u0430\u0434\u0440\u0435\u0441\u0456 \u043f\u043e\u0442\u0440\u0456\u0431\u0435\u043d \u0456\u043d\u0434\u0435\u043a\u0441: 00-000",
            "pl": "W adresie podaj kod pocztowy: 00-000",
        },
        "required": {
            "ru": "\u041f\u043e\u043b\u0435 \u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e",
            "en": "This field is required",
            "ua": "\u041f\u043e\u043b\u0435 \u043e\u0431\u043e\u0432'\u044f\u0437\u043a\u043e\u0432\u0435",
            "pl": "To pole jest wymagane",
        },
        "money": {
            "ru": "\u0421\u0443\u043c\u043c\u0430 \u2014 \u0442\u043e\u043b\u044c\u043a\u043e \u0447\u0438\u0441\u043b\u043e, \u043d\u0430\u043f\u0440. 3500",
            "en": "Amount: numbers only, e.g. 3500",
            "ua": "\u0421\u0443\u043c\u0430 \u2014 \u043b\u0438\u0448\u0435 \u0447\u0438\u0441\u043b\u043e, \u043d\u0430\u043f\u0440. 3500",
            "pl": "Kwota: sam numer, np. 3500",
        },
    }
    block = msgs.get(key, {})
    return block.get(lang, block.get("ru", ""))


def is_required(key: str) -> bool:
    return key not in OPTIONAL_FIELDS


def _valid_date(value: str) -> bool:
    if not DATE_RE.match(value):
        return False
    try:
        datetime.strptime(value, "%d.%m.%Y")
        return True
    except ValueError:
        return False


def validate_field(key: str, value: str, lang: str) -> str | None:
    v = value.strip()
    if not v:
        return _msg("required", lang) if is_required(key) else None

    if key in DATE_FIELDS and not _valid_date(v):
        return _msg("date", lang)

    if key == "pesel" and v.lower() not in PESEL_SKIP:
        if not PESEL_RE.match(v.replace(" ", "")):
            return _msg("pesel", lang)

    if key == "adres_zamieszkania" and not POSTAL_RE.search(v):
        return _msg("postal", lang)

    if key in MONEY_FIELDS:
        clean = v.replace(" ", "").replace(",", ".")
        if not MONEY_RE.match(clean):
            return _msg("money", lang)

    return None
