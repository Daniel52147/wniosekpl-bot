"""Статические подсказки к полям (без AI)."""

FIELD_EXPLAIN: dict[str, dict[str, str]] = {
    "imie": {
        "ru": "Имя латиницей, как в паспорте. В urzędzie — WIELKIE LITERY.",
        "en": "First name in Latin, as in passport. Offices often use UPPERCASE.",
        "ua": "Ім'я латиницею, як у паспорті. В urzędzie — WIELKIE LITERY.",
        "pl": "Imię łaciną jak w paszporcie. W urzędzie — WIELKIE LITERY.",
    },
    "nazwisko": {
        "ru": "Фамилия как в документе. Без сокращений.",
        "en": "Last name as in ID document. No abbreviations.",
        "ua": "Прізвище як у документі. Без скорочень.",
        "pl": "Nazwisko jak w dokumencie tożsamości.",
    },
    "adres_zamieszkania": {
        "ru": "Формат: ulica numer, 00-000 miasto. Пример: ul. Marszałkowska 10/5, 00-001 Warszawa",
        "en": "Format: street number, 00-000 city. E.g. ul. Marszałkowska 10/5, 00-001 Warszawa",
        "ua": "Формат: ulica numer, 00-000 miasto. Напр.: ul. Marszałkowska 10/5, 00-001 Warszawa",
        "pl": "ulica, numer, kod pocztowy, miejscowość — np. ul. Marszałkowska 10, 00-001 Warszawa",
    },
    "podstawa_prawna": {
        "ru": "§7 wniosku PESEL — обязательно. Возьмите формулировку из письма ZUS, urzędu или pracodawcy.",
        "en": "§7 PESEL application — mandatory. Copy wording from ZUS, office or employer.",
        "ua": "§7 wniosku PESEL — обов'язково. Візьміть формулювання з ZUS, urzędu або pracodawcy.",
        "pl": "§7 wniosku PESEL — obowiązkowe. Przepis podaje ZUS, urząd lub pracodawca.",
    },
    "pesel": {
        "ru": "11 цифр, если уже есть. Если нет — напишите: brak",
        "en": "11 digits if you have one. Otherwise type: brak",
        "ua": "11 цифр, якщо є. Якщо ні — напишіть: brak",
        "pl": "11 cyfr jeśli masz. Jeśli nie — wpisz: brak",
    },
    "wlasciciel_nieruchomosci": {
        "ru": "Владелец подписывает formularz meldunkowy (§5). Без подписи — риск отказа.",
        "en": "Landlord signs the meldunek form (§5). Without signature — risk of rejection.",
        "ua": "Власник підписує formularz meldunkowy (§5). Без підпису — ризик відмови.",
        "pl": "Właściciel podpisuje formularz (§5). Bez podpisu urząd może odmówić.",
    },
    "czynsz": {
        "ru": "Сумма в злотых, только число, например: 3500",
        "en": "Amount in PLN, numbers only, e.g. 3500",
        "ua": "Сума в злотих, лише число, напр. 3500",
        "pl": "Kwota w PLN, sam numer, np. 3500",
    },
    "data_urodzenia": {
        "ru": "Формат DD.MM.RRRR — например 15.03.1990",
        "en": "Format DD.MM.RRRR — e.g. 15.03.1990",
        "ua": "Формат DD.MM.RRRR — напр. 15.03.1990",
        "pl": "Format DD.MM.RRRR — np. 15.03.1990",
    },
    "numer_paszportu": {
        "ru": "Серия и номер как в паспорте, латиницей.",
        "en": "Passport series and number, Latin letters.",
        "ua": "Серія та номер як у паспорті, латиницею.",
        "pl": "Seria i numer jak w paszporcie.",
    },
    "data_wjazdu": {
        "ru": "Дата первого въезда в Польшу — DD.MM.RRRR",
        "en": "Date of first entry to Poland — DD.MM.RRRR",
        "ua": "Дата першого в'їзду до Польщі — DD.MM.RRRR",
        "pl": "Data wjazdu do Polski — DD.MM.RRRR",
    },
    "data_zameldowania": {
        "ru": "Дата meldunku — DD.MM.RRRR (сегодня или планируемая)",
        "en": "Meldunek date — DD.MM.RRRR (today or planned)",
        "ua": "Дата meldunku — DD.MM.RRRR",
        "pl": "Data zameldowania — DD.MM.RRRR",
    },
}


def explain_field(field_key: str, lang: str) -> str:
    block = FIELD_EXPLAIN.get(field_key, {})
    return block.get(lang, block.get("ru", ""))
