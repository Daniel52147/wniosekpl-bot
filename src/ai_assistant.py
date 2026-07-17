"""Rule-based assistant MVP for common foreigner-in-Poland questions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AssistantAnswer:
    topic: str
    text: str


_DISCLAIMER = {
    "ru": "⚠️ Это информационная подсказка, не юридическая консультация.",
    "en": "⚠️ This is informational help, not legal advice.",
    "ua": "⚠️ Це інформаційна підказка, не юридична консультація.",
    "pl": "⚠️ To informacyjna pomoc, nie porada prawna.",
}


_TOPICS: dict[str, dict[str, list[str] | dict[str, str]]] = {
    "karta_pobytu": {
        "keywords": [
            "karta",
            "pobytu",
            "карта",
            "побыту",
            "побиту",
            "residence",
            "zezwolenie",
        ],
        "answers": {
            "ru": (
                "<b>Karta pobytu: что подготовить</b>\n\n"
                "1. Паспорт + копии страниц с данными и визами/штампами.\n"
                "2. Заполненный wniosek и актуальные фото.\n"
                "3. Основание пребывания: работа, учёба, бизнес или семья.\n"
                "4. Подтверждение дохода и страховки.\n"
                "5. Подтверждение адреса в Польше.\n\n"
                "Следующий шаг: соберите договор/справки и проверьте список на сайте вашего urzędu wojewódzkiego."
            ),
            "en": (
                "<b>Residence card: what to prepare</b>\n\n"
                "1. Passport and copies of relevant pages.\n"
                "2. Completed application form and current photos.\n"
                "3. Basis of stay: work, studies, business, or family.\n"
                "4. Income and insurance proof.\n"
                "5. Address proof in Poland.\n\n"
                "Next step: collect contracts/certificates and verify the list on your voivodeship office website."
            ),
            "ua": (
                "<b>Karta pobytu: що підготувати</b>\n\n"
                "1. Паспорт і копії сторінок.\n"
                "2. Заповнений wniosek і актуальні фото.\n"
                "3. Підстава перебування: робота, навчання, бізнес або сім'я.\n"
                "4. Підтвердження доходу та страхування.\n"
                "5. Підтвердження адреси в Польщі.\n\n"
                "Наступний крок: звірте список на сайті вашого urzędu wojewódzkiego."
            ),
            "pl": (
                "<b>Karta pobytu: co przygotować</b>\n\n"
                "1. Paszport i kopie ważnych stron.\n"
                "2. Wypełniony wniosek i aktualne zdjęcia.\n"
                "3. Podstawa pobytu: praca, studia, firma albo rodzina.\n"
                "4. Potwierdzenie dochodu i ubezpieczenia.\n"
                "5. Potwierdzenie adresu w Polsce.\n\n"
                "Następny krok: sprawdź szczegółową listę na stronie swojego urzędu wojewódzkiego."
            ),
        },
    },
    "pesel": {
        "keywords": ["pesel", "песель", "песел"],
        "answers": {
            "ru": (
                "<b>PESEL: коротко</b>\n\n"
                "Обычно нужны: документ личности, адрес в Польше, meldunek или основание для PESEL, "
                "а также заполненный wniosek.\n\n"
                "В WniosekPL можно сразу создать PDF: /docs → PESEL."
            ),
            "en": (
                "<b>PESEL: short checklist</b>\n\n"
                "Usually needed: identity document, Polish address, meldunek or legal basis for PESEL, "
                "and a completed application.\n\n"
                "You can create the PDF in WniosekPL: /docs → PESEL."
            ),
            "ua": (
                "<b>PESEL: коротко</b>\n\n"
                "Зазвичай потрібні: документ особи, адреса в Польщі, meldunek або підстава для PESEL, "
                "і заповнений wniosek.\n\n"
                "PDF можна створити тут: /docs → PESEL."
            ),
            "pl": (
                "<b>PESEL: krótka checklista</b>\n\n"
                "Zwykle potrzebne są: dokument tożsamości, adres w Polsce, meldunek albo podstawa prawna, "
                "oraz wypełniony wniosek.\n\n"
                "PDF utworzysz w WniosekPL: /docs → PESEL."
            ),
        },
    },
    "office_letter": {
        "keywords": [
            "письмо",
            "ужонд",
            "urząd",
            "wezwanie",
            "decyzja",
            "odmowa",
            "отказ",
            "letter",
        ],
        "answers": {
            "ru": (
                "<b>Письмо из urzędu: что сделать</b>\n\n"
                "1. Найдите срок: часто это 7 или 14 дней.\n"
                "2. Проверьте, что именно требуют: документ, подпись, оплату или объяснение.\n"
                "3. Не игнорируйте письмо, даже если это не отказ.\n"
                "4. Если нужен ответ, можно подготовить официальное письмо на польском.\n\n"
                "MVP пока не читает фото. Пришлите ключевые фразы текстом — я помогу понять смысл."
            ),
            "en": (
                "<b>Office letter: what to do</b>\n\n"
                "1. Find the deadline, often 7 or 14 days.\n"
                "2. Check what is requested: document, signature, payment, or explanation.\n"
                "3. Do not ignore it, even if it is not a refusal.\n"
                "4. If needed, prepare an official Polish response.\n\n"
                "This MVP does not read photos yet. Send the key phrases as text."
            ),
            "ua": (
                "<b>Лист з urzędu: що зробити</b>\n\n"
                "1. Знайдіть строк: часто 7 або 14 днів.\n"
                "2. Перевірте, що саме вимагають: документ, підпис, оплату чи пояснення.\n"
                "3. Не ігноруйте лист, навіть якщо це не відмова.\n\n"
                "MVP поки не читає фото. Надішліть ключові фрази текстом."
            ),
            "pl": (
                "<b>Pismo z urzędu: co zrobić</b>\n\n"
                "1. Znajdź termin — często 7 albo 14 dni.\n"
                "2. Sprawdź, czego urząd żąda: dokumentu, podpisu, opłaty albo wyjaśnienia.\n"
                "3. Nie ignoruj pisma, nawet jeśli to nie odmowa.\n\n"
                "MVP nie czyta jeszcze zdjęć. Wyślij kluczowe zdania tekstem."
            ),
        },
    },
    "zus_nfz": {
        "keywords": ["zus", "nfz", "страх", "ubezpiec", "insurance", "lekarz", "врач"],
        "answers": {
            "ru": (
                "<b>ZUS / NFZ: базово</b>\n\n"
                "Если вы работаете официально, работодатель обычно регистрирует вас в ZUS. "
                "Медицинский доступ NFZ зависит от действующей страховки.\n\n"
                "Проверьте: umowa, zgłoszenie do ZUS, статус у работодателя или в IKP."
            ),
            "en": (
                "<b>ZUS / NFZ basics</b>\n\n"
                "With legal employment, the employer usually registers you in ZUS. "
                "NFZ medical access depends on active insurance.\n\n"
                "Check your contract, ZUS registration, employer confirmation, or IKP."
            ),
            "ua": (
                "<b>ZUS / NFZ: базово</b>\n\n"
                "Якщо ви працюєте офіційно, роботодавець зазвичай реєструє вас у ZUS. "
                "Доступ до NFZ залежить від активного страхування."
            ),
            "pl": (
                "<b>ZUS / NFZ: podstawy</b>\n\n"
                "Przy legalnej pracy pracodawca zwykle zgłasza Cię do ZUS. "
                "Dostęp do NFZ zależy od aktywnego ubezpieczenia.\n\n"
                "Sprawdź umowę, zgłoszenie ZUS, potwierdzenie pracodawcy albo IKP."
            ),
        },
    },
}


_FALLBACK = {
    "ru": (
        "<b>Я могу помочь с вопросами о документах в Польше</b>\n\n"
        "Лучше всего спросить конкретно: PESEL, meldunek, karta pobytu, ZUS/NFZ, "
        "письмо из urzędu или официальный ответ на польском.\n\n"
        "Пример: «Я гражданин Украины, работаю официально, хочу карту побыту»."
    ),
    "en": (
        "<b>I can help with paperwork questions in Poland</b>\n\n"
        "Ask about PESEL, meldunek, residence card, ZUS/NFZ, office letters, "
        "or official Polish responses.\n\n"
        "Example: “I am Ukrainian, legally employed, and need a residence card”."
    ),
    "ua": (
        "<b>Я можу допомогти з документами в Польщі</b>\n\n"
        "Запитайте про PESEL, meldunek, karta pobytu, ZUS/NFZ або лист з urzędu."
    ),
    "pl": (
        "<b>Mogę pomóc z dokumentami w Polsce</b>\n\n"
        "Zapytaj o PESEL, meldunek, kartę pobytu, ZUS/NFZ, pismo z urzędu "
        "albo odpowiedź urzędową po polsku."
    ),
}


def answer_question(question: str, lang: str) -> AssistantAnswer:
    normalized = (question or "").casefold()
    safe_lang = lang if lang in ("ru", "en", "ua", "pl") else "ru"

    for topic, data in _TOPICS.items():
        keywords = data["keywords"]
        if any(keyword in normalized for keyword in keywords):
            answers = data["answers"]
            body = answers.get(safe_lang, answers["ru"])
            return AssistantAnswer(topic=topic, text=f"{body}\n\n{_DISCLAIMER[safe_lang]}")

    return AssistantAnswer(
        topic="fallback",
        text=f"{_FALLBACK[safe_lang]}\n\n{_DISCLAIMER[safe_lang]}",
    )
