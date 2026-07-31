KARTA_STEPS = [
    {"id": "passport_copies", "ru": "Паспорт + копии всех страниц", "en": "Passport + copies", "ua": "Паспорт + копії", "pl": "Paszport + kopie"},
    {"id": "photos", "ru": "4 фото 35×45 мм", "en": "4 photos 35×45 mm", "ua": "4 фото 35×45", "pl": "4 zdjęcia 35×45"},
    {"id": "application", "ru": "Подготовить данные к MOS 2.0 (не бумажный blankiet)", "en": "Prepare data for MOS 2.0 (not a paper form)", "ua": "Підготувати дані до MOS 2.0", "pl": "Przygotuj dane do MOS 2.0 (nie papierowy blankiet)"},
    {"id": "insurance", "ru": "Страховка ZUS / NFZ / prywatная", "en": "Insurance proof", "ua": "Страхування", "pl": "Ubezpieczenie"},
    {"id": "address", "ru": "Адрес / meldunek / umowa najmu", "en": "Address / meldunek / rental", "ua": "Адреса / meldunek", "pl": "Adres / meldunek / umowa"},
    {"id": "income", "ru": "Доходы / umowa o pracę / oświadczenie", "en": "Income / employment proof", "ua": "Доходи", "pl": "Dochody / umowa"},
    {"id": "fee", "ru": "Оплатить opłatę skarbową", "en": "Pay stamp duty", "ua": "Сплатити opłatę", "pl": "Opłata skarbowa"},
    {"id": "submit", "ru": "Подать online в MOS 2.0 до конца легального pobytu", "en": "File online in MOS 2.0 before stay expires", "ua": "Подати online в MOS 2.0 до кінця pobytu", "pl": "Złóż online w MOS 2.0 przed końcem legalnego pobytu"},
]


def default_progress() -> dict[str, bool]:
    return {step["id"]: False for step in KARTA_STEPS}


def progress_view(steps: dict[str, bool], lang: str = "ru") -> list[dict]:
    merged = default_progress()
    merged.update(steps or {})
    view = []
    for step in KARTA_STEPS:
        view.append(
            {
                "id": step["id"],
                "title": step.get(lang, step["ru"]),
                "done": bool(merged.get(step["id"])),
            }
        )
    return view
