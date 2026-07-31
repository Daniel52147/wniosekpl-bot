CHECKLISTS: dict[str, dict[str, str]] = {
    "pesel": {
        "ru": (
            "<b>Чеклист перед urzędem (PESEL)</b>\n"
            "☐ Распечатанный и подписанный wniosek\n"
            "☐ Паспорт (oryginał)\n"
            "☐ Meldunek или адрес в Польше\n"
            "☐ §7 podstawa prawna — как в требовании ZUS/urzędu/pracodawcy\n"
            "☐ Копии документов, если urząd попросит\n"
            "☐ Urząd gminy: meldunek lub siedziba pracodawcy"
        ),
        "en": (
            "<b>Before the office (PESEL)</b>\n"
            "☐ Printed, signed application\n"
            "☐ Passport (original)\n"
            "☐ Registration address in Poland\n"
            "☐ §7 legal basis as required by ZUS/office/employer\n"
            "☐ Commune office (gmina) per your situation"
        ),
        "ua": (
            "<b>Чекліст (PESEL)</b>\n"
            "☐ Друкований і підписаний wniosek\n"
            "☐ Паспорт\n"
            "☐ §7 podstawa prawna\n"
            "☐ Urząd gminy"
        ),
        "pl": (
            "<b>Checklista PESEL</b>\n"
            "☐ Wydrukowany i podpisany wniosek\n"
            "☐ Paszport (oryginał)\n"
            "☐ Adres zameldowania w Polsce\n"
            "☐ §7 podstawa prawna — jak w ZUS/urzędzie\n"
            "☐ Urząd gminy lub siedziba pracodawcy"
        ),
    },
    "meldunek": {
        "ru": (
            "<b>Чеклист (Meldunek EL/ZC/1)</b>\n"
            "☐ Формуляр с <b>подписью właściciela</b> lokalu (§5)\n"
            "☐ Паспорт / dokument podróży\n"
            "☐ Umowa najmu или tytuł prawny do lokalu\n"
            "☐ Zaświadczenie o meldunku — <b>17 zł</b> opłata skarbowa (jeśli potrzebujesz)\n"
            "☐ Urząd gminy przy adresie mieszkania\n"
            "☐ Zamelduj się w ciągu 30 dni od przyjazdu"
        ),
        "en": (
            "<b>Checklist (Meldunek EL/ZC/1)</b>\n"
            "☐ Form with <b>landlord signature</b> (§5)\n"
            "☐ Passport / travel document\n"
            "☐ Rental contract or title to the flat\n"
            "☐ Certificate fee <b>17 PLN</b> if needed\n"
            "☐ Commune office for your address"
        ),
        "ua": (
            "<b>Чекліст (Meldunek)</b>\n"
            "☐ Формуляр з підписом власника\n"
            "☐ Паспорт, umowa najmu\n"
            "☐ 17 zł — zaświadczenie (за потреби)"
        ),
        "pl": (
            "<b>Checklista meldunku EL/ZC/1</b>\n"
            "☐ Formularz z <b>podpisem właściciela</b> (§5)\n"
            "☐ Paszport / dokument podróży\n"
            "☐ Umowa najmu lub tytuł prawny\n"
            "☐ Zaświadczenie o meldunku — <b>17 zł</b> (jeśli potrzebujesz)\n"
            "☐ Urząd gminy przy adresie mieszkania\n"
            "☐ Zamelduj się w ciągu 30 dni od przyjazdu"
        ),
    },
    "meldunek_staly": {
        "ru": (
            "<b>Чеклист (Meldunek EL/ZPS/1 — stały)</b>\n"
            "☐ Podpis właściciela na formularzu\n"
            "☐ Paszport, tytuł prawny do lokalu\n"
            "☐ Urząd gminy — adres nieruchomości\n"
            "☐ Zaświadczenie: 17 zł jeśli potrzebujesz"
        ),
        "en": "<b>EL/ZPS/1 permanent</b>\n☐ Landlord signature\n☐ Passport, title to flat\n☐ Gmina office",
        "ua": "<b>EL/ZPS/1 stały</b>\n☐ Підпис власника\n☐ Паспорт",
    },
    "umowa_najmu": {
        "ru": (
            "<b>Чеклист (Umowa najmu)</b>\n"
            "☐ 2 экземпляра — по одному каждой стороне\n"
            "☐ Подписи najemcy i wynajmującego\n"
            "☐ Проверьте kaucję, media, okres najmu\n"
            "☐ Это szablon — przy wątpliwościach prawnik"
        ),
        "en": (
            "<b>Checklist (Rental agreement)</b>\n"
            "☐ Two copies, both parties sign\n"
            "☐ Check deposit, utilities, term\n"
            "☐ Template only — lawyer if unsure"
        ),
        "ua": (
            "<b>Чекліст (Umowa)</b>\n"
            "☐ 2 примірники, підписи сторін\n"
            "☐ Szablon — юрист за потреби"
        ),
        "pl": (
            "<b>Checklista umowy najmu</b>\n"
            "☐ 2 egzemplarze — po jednym dla stron\n"
            "☐ Podpisy najemcy i wynajmującego\n"
            "☐ Sprawdź kaucję, media, okres najmu\n"
            "☐ Szablon — przy wątpliwościach prawnik"
        ),
    },
    "karta_pobytu": {
        "ru": (
            "<b>Чеклист Karta pobytu (подготовка)</b>\n"
            "☐ Wniosek o kartę pobytu — właściwy wzór (cel pobytu)\n"
            "☐ Paszport + kopie wszystkich stron\n"
            "☐ 4 zdjęcia 35×45 mm\n"
            "☐ Ubezpieczenie ZUS / praca / uczelnia\n"
            "☐ Zaświadczenie o meldunku (17 zł)\n"
            "☐ Umowa najmu / tytuł prawny do lokalu\n"
            "☐ Zaświadczenie o dochodach / praca / uczelnia\n"
            "☐ Opłata skarbowa za wniosek\n"
            "☐ Termin: złóż przed końcem legalnego pobytu\n\n"
            "<i>WniosekPL — формуляр wkrótce. Zapisz się w menu.</i>"
        ),
        "en": (
            "<b>Residence card checklist</b>\n"
            "☐ Correct application form for your purpose\n"
            "☐ Passport + copies of all pages\n"
            "☐ 4 photos 35×45 mm\n"
            "☐ Health insurance (ZUS / work / university)\n"
            "☐ Meldunek certificate (17 PLN)\n"
            "☐ Rental contract / title to flat\n"
            "☐ Proof of income / work / studies\n"
            "☐ Stamp duty fee\n"
            "☐ File before your legal stay expires"
        ),
        "ua": (
            "<b>Чекліст Karta pobytu</b>\n"
            "☐ Правильний wniosek за метою перебування\n"
            "☐ Паспорт + копії всіх сторінок\n"
            "☐ 4 фото 35×45 мм\n"
            "☐ Страхування ZUS / робота / навчання\n"
            "☐ Zaświadczenie o meldunku (17 zł)\n"
            "☐ Umowa najmu\n"
            "☐ Дохід / робота / навчання\n"
            "☐ Оплата skarbowa\n"
            "☐ Подати до закінчення легального перебування"
        ),
        "pl": (
            "<b>Checklista Karta pobytu</b>\n"
            "☐ Właściwy wzór wniosku (cel pobytu)\n"
            "☐ Paszport + kopie wszystkich stron\n"
            "☐ 4 zdjęcia 35×45 mm\n"
            "☐ Ubezpieczenie ZUS / praca / uczelnia\n"
            "☐ Zaświadczenie o meldunku (17 zł)\n"
            "☐ Umowa najmu / tytuł prawny\n"
            "☐ Zaświadczenie o dochodach\n"
            "☐ Opłata skarbowa\n"
            "☐ Złóż przed końcem legalnego pobytu"
        ),
    },
    "zus": {
        "ru": (
            "<b>Чеклист ZUS (после meldunku)</b>\n"
            "☐ ZUS ZUA / ZUA — zgłoszenie do ubezpieczeń (pracodawca lub sam)\n"
            "☐ Paszport, meldunek, umowa o pracę / działalność\n"
            "☐ Numer rachunku bankowego (PL)\n"
            "☐ Adres korespondencyjny = adres zameldowania\n"
            "☐ Ubezpieczenie zdrowotne — potrzebne do PESEL i karty pobytu"
        ),
        "en": (
            "<b>ZUS checklist (after meldunek)</b>\n"
            "☐ ZUS registration (employer or self)\n"
            "☐ Passport, meldunek, work contract\n"
            "☐ Polish bank account\n"
            "☐ Health insurance — needed for PESEL & residence card"
        ),
        "ua": (
            "<b>Чекліст ZUS</b>\n"
            "☐ Реєстрація ZUS (pracodawca або сам)\n"
            "☐ Паспорт, meldunek, umowa\n"
            "☐ Банківський рахунок PL"
        ),
        "pl": (
            "<b>Checklista ZUS (po meldunku)</b>\n"
            "☐ Zgłoszenie do ZUS (pracodawca lub sam)\n"
            "☐ Paszport, meldunek, umowa o pracę\n"
            "☐ Rachunek bankowy PL\n"
            "☐ Ubezpieczenie zdrowotne — potrzebne do PESEL i karty pobytu"
        ),
    },
    "przeprowadzka": {
        "ru": (
            "<b>Пакет «Переезд» — порядок в urzędzie</b>\n"
            "1️⃣ Подписать umowę z właścicielem\n"
            "2️⃣ Meldunek + podpis właściciela na formularzu\n"
            "3️⃣ PESEL w gminie (z podstawą prawną)\n"
            "☐ Паспорт всегда с собой\n"
            "☐ Zaświadczenie meldunkowe: 17 zł\n"
            "⚠️ Pomocnik — nie urząd"
        ),
        "en": (
            "<b>Relocation package — order</b>\n"
            "1️⃣ Sign rental agreement\n"
            "2️⃣ Meldunek + landlord signature\n"
            "3️⃣ PESEL at gmina with legal basis\n"
            "☐ Passport; meldunek certificate 17 PLN"
        ),
        "ua": (
            "<b>Пакет «Переїзд»</b>\n"
            "1️⃣ Umowa 2️⃣ Meldunek 3️⃣ PESEL\n"
            "☐ Підпис власника, 17 zł"
        ),
        "pl": (
            "<b>Pakiet Przeprowadzka — kolejność</b>\n"
            "1️⃣ Podpisz umowę z właścicielem\n"
            "2️⃣ Meldunek + podpis właściciela\n"
            "3️⃣ PESEL w gminie (z podstawą prawną)\n"
            "☐ Paszport; zaświadczenie meldunkowe: 17 zł"
        ),
    },
    "pismo_do_urzedu": {
        "ru": (
            "<b>Чеклист (Pismo do urzędu)</b>\n"
            "☐ Дата и znak sprawy (если есть)\n"
            "☐ Чёткая просьба / ответ на wezwanie\n"
            "☐ Копии приложений\n"
            "☐ Подпись и телефон"
        ),
        "en": (
            "<b>Checklist (Office letter)</b>\n"
            "☐ Date and case number if available\n"
            "☐ Clear request / reply to summons\n"
            "☐ Copies of attachments\n"
            "☐ Signature and phone"
        ),
        "ua": "<b>Чекліст (Pismo)</b>\n☐ Дата, znak sprawy\n☐ Копії\n☐ Підпис",
        "pl": (
            "<b>Checklista (Pismo do urzędu)</b>\n"
            "☐ Data i znak sprawy\n"
            "☐ Jasna prośba / odpowiedź na wezwanie\n"
            "☐ Kopie załączników\n"
            "☐ Podpis i telefon"
        ),
    },
    "upowaznienie": {
        "ru": (
            "<b>Чеклист (Upoważnienie)</b>\n"
            "☐ Dane mocodawcy i pełnomocnika\n"
            "☐ Чёткий zakres\n"
            "☐ Подпись mocodawcy\n"
            "☐ Если urząd требует notarialne — этот szablon не подойдёт"
        ),
        "en": (
            "<b>Checklist (Authorization)</b>\n"
            "☐ Principal and attorney details\n"
            "☐ Clear scope\n"
            "☐ Principal signature\n"
            "☐ Notarial form may be required"
        ),
        "ua": "<b>Чекліст (Upoważnienie)</b>\n☐ Дані сторін\n☐ Zakres\n☐ Підпис",
        "pl": (
            "<b>Checklista (Upoważnienie)</b>\n"
            "☐ Dane mocodawcy i pełnomocnika\n"
            "☐ Jasny zakres\n"
            "☐ Podpis mocodawcy\n"
            "☐ Jeśli urząd wymaga notarialnego — ten szablon nie wystarczy"
        ),
    },
    "oswiadczenie_dochodow": {
        "ru": (
            "<b>Чеклист (Oświadczenie o dochodach)</b>\n"
            "☐ Источник дохода и сумма netto\n"
            "☐ Период\n"
            "☐ Приложите umowę / PIT если urząd просит\n"
            "☐ Подпись"
        ),
        "en": (
            "<b>Checklist (Income declaration)</b>\n"
            "☐ Income source and net amount\n"
            "☐ Covered period\n"
            "☐ Attach employment / tax proof if requested\n"
            "☐ Signature"
        ),
        "ua": "<b>Чекліст (Dochody)</b>\n☐ Джерело і сума\n☐ Період\n☐ Підпис",
        "pl": (
            "<b>Checklista (Oświadczenie o dochodach)</b>\n"
            "☐ Źródło dochodu i kwota netto\n"
            "☐ Okres\n"
            "☐ Dołącz umowę / PIT jeśli urząd wymaga\n"
            "☐ Podpis"
        ),
    },
}


def checklist(doc_id: str, lang: str) -> str:
    block = CHECKLISTS.get(doc_id, {})
    return block.get(lang, block.get("ru", ""))
