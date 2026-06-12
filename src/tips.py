"""Common mistakes shown after PDF generation."""

TIPS: dict[str, dict[str, str]] = {
    "pesel": {
        "ru": (
            "\u26a0\ufe0f <b>\u0427\u0430\u0441\u0442\u044b\u0435 \u043e\u0448\u0438\u0431\u043a\u0438 PESEL:</b>\n"
            "\u2022 \u041f\u0443\u0441\u0442\u043e\u0439 \u00a77 podstawa prawna \u2014 urz\u0105d \u043e\u0442\u043a\u0430\u0436\u0435\u0442\n"
            "\u2022 \u0418\u043c\u044f \u043d\u0435 \u043a\u0430\u043a \u0432 \u043f\u0430\u0441\u043f\u043e\u0440\u0442\u0435\n"
            "\u2022 \u041d\u0435\u0442 \u043f\u043e\u0434\u043f\u0438\u0441\u0438 \u043d\u0430 wniosku"
        ),
        "en": (
            "\u26a0\ufe0f <b>Common PESEL mistakes:</b>\n"
            "\u2022 Empty \u00a77 legal basis\n"
            "\u2022 Name doesn't match passport\n"
            "\u2022 Missing signature"
        ),
        "ua": (
            "\u26a0\ufe0f <b>\u0422\u0438\u043f\u043e\u0432\u0456 \u043f\u043e\u043c\u0438\u043b\u043a\u0438 PESEL:</b>\n"
            "\u2022 \u041f\u043e\u0440\u043e\u0436\u043d\u0456\u0439 \u00a77 podstawa prawna\n"
            "\u2022 \u0406\u043c'\u044f \u043d\u0435 \u044f\u043a \u0443 \u043f\u0430\u0441\u043f\u043e\u0440\u0442\u0456"
        ),
        "pl": (
            "\u26a0\ufe0f <b>Typowe b\u0142\u0119dy PESEL:</b>\n"
            "\u2022 Brak \u00a77 podstawy prawnej\n"
            "\u2022 Imi\u0119 inne ni\u017c w paszporcie\n"
            "\u2022 Brak podpisu"
        ),
    },
    "meldunek": {
        "ru": (
            "\u26a0\ufe0f <b>\u0427\u0430\u0441\u0442\u044b\u0435 \u043e\u0448\u0438\u0431\u043a\u0438 Meldunek:</b>\n"
            "\u2022 \u041d\u0435\u0442 \u043f\u043e\u0434\u043f\u0438\u0441\u0438 w\u0142a\u015bciciela (\u00a75)\n"
            "\u2022 \u0410\u0434\u0440\u0435\u0441 \u043d\u0435 \u0441\u043e\u0432\u043f\u0430\u0434\u0430\u0435\u0442 \u0441 umow\u0105\n"
            "\u2022 \u041f\u0440\u043e\u0441\u0440\u043e\u0447\u0435\u043d 30-\u0434\u043d\u0435\u0432\u043d\u044b\u0439 \u0441\u0440\u043e\u043a"
        ),
        "en": (
            "\u26a0\ufe0f <b>Common Meldunek mistakes:</b>\n"
            "\u2022 No landlord signature (\u00a75)\n"
            "\u2022 Address mismatch\n"
            "\u2022 Missed 30-day deadline"
        ),
        "ua": (
            "\u26a0\ufe0f <b>\u0422\u0438\u043f\u043e\u0432\u0456 \u043f\u043e\u043c\u0438\u043b\u043a\u0438 Meldunek:</b>\n"
            "\u2022 \u041d\u0435\u043c\u0430\u0454 \u043f\u0456\u0434\u043f\u0438\u0441\u0443 \u0432\u043b\u0430\u0441\u043d\u0438\u043a\u0430\n"
            "\u2022 \u0410\u0434\u0440\u0435\u0441\u0430 \u043d\u0435 \u0437\u0431\u0456\u0433\u0430\u0454\u0442\u044c\u0441\u044f"
        ),
        "pl": (
            "\u26a0\ufe0f <b>Typowe b\u0142\u0119dy meldunku:</b>\n"
            "\u2022 Brak podpisu w\u0142a\u015bciciela (\u00a75)\n"
            "\u2022 Adres niezgodny z umow\u0105"
        ),
    },
    "meldunek_staly": {
        "ru": "\u26a0\ufe0f Meldunek sta\u0142y \u2014 \u043d\u0443\u0436\u0435\u043d tytu\u0142 prawny do lokalu \u0438 \u043f\u043e\u0434\u043f\u0438\u0441\u044c w\u0142a\u015bciciela.",
        "en": "\u26a0\ufe0f Permanent meldunek \u2014 title to flat + landlord signature required.",
        "ua": "\u26a0\ufe0f Pobyt sta\u0142y \u2014 tytu\u0142 prawny + \u043f\u0456\u0434\u043f\u0438\u0441 \u0432\u043b\u0430\u0441\u043d\u0438\u043a\u0430.",
        "pl": "\u26a0\ufe0f Meldunek sta\u0142y \u2014 tytu\u0142 prawny do lokalu i podpis w\u0142a\u015bciciela.",
    },
    "umowa_najmu": {
        "ru": "\u26a0\ufe0f Umowa \u2014 szablon pomocniczy. \u041f\u0440\u043e\u0432\u0435\u0440\u044c\u0442\u0435 kaucj\u0119, media, okres najmu.",
        "en": "\u26a0\ufe0f Rental template \u2014 verify deposit, utilities, term.",
        "ua": "\u26a0\ufe0f Umowa \u2014 szablon. \u041f\u0435\u0440\u0435\u0432\u0456\u0440\u0442\u0435 kaucj\u0119 \u0442\u0430 media.",
        "pl": "\u26a0\ufe0f Umowa \u2014 szablon pomocniczy. Sprawd\u017a kaucj\u0119 i media.",
    },
}


def tip_after_pdf(doc_id: str, lang: str) -> str:
    block = TIPS.get(doc_id, {})
    return block.get(lang, block.get("ru", ""))
