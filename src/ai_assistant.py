"""Rule-based assistant MVP for common foreigner-in-Poland questions."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class AssistantAnswer:
    topic: str
    text: str
    actions: tuple[dict, ...] = field(default_factory=tuple)


_DISCLAIMER = {
    "ru": "⚠️ Это информационная подсказка, не юридическая консультация.",
    "en": "⚠️ This is informational help, not legal advice.",
    "ua": "⚠️ Це інформаційна підказка, не юридична консультація.",
    "pl": "⚠️ To informacyjna pomoc, nie porada prawna.",
}


def _L(pl: str, ru: str, en: str, ua: str) -> dict[str, str]:
    return {"pl": pl, "ru": ru, "en": en, "ua": ua}


def _doc(doc_id: str, labels: dict[str, str]) -> dict:
    return {"type": "open_doc", "id": doc_id, "label": labels}


def _goto(target: str, href: str, labels: dict[str, str]) -> dict:
    return {"type": "goto", "id": target, "href": href, "label": labels}


_TOPIC_ACTIONS: dict[str, list[dict]] = {
    "pesel": [
        _doc("pesel", _L("Wypełnij PESEL", "Заполнить PESEL", "Fill PESEL", "Заповнити PESEL")),
        _goto("mos", "#mos", _L("Checklist MOS", "Чеклист MOS", "MOS checklist", "Чекліст MOS")),
    ],
    "karta_pobytu": [
        _goto("mos", "#mos", _L("Przygotuj MOS", "Подготовка к MOS", "Prepare MOS", "Підготовка до MOS")),
        _doc(
            "karta_pobytu_przygotowanie",
            _L("Checklist karty", "Чеклист karty", "Card checklist", "Чекліст karty"),
        ),
        _doc(
            "oswiadczenie_dochodow",
            _L("Oświadczenie o dochodach", "Заявление о доходах", "Income declaration", "Заява про доходи"),
        ),
    ],
    "office_letter": [
        _doc(
            "pismo_do_urzedu",
            _L("Napisz pismo do urzędu", "Написать письмо в urząd", "Write office letter", "Написати лист до urzędu"),
        ),
    ],
    "upowaznienie": [
        _doc(
            "upowaznienie",
            _L("Szablon upoważnienia", "Шаблон доверенности", "Authorization template", "Шаблон довіреності"),
        ),
    ],
    "dochody": [
        _doc(
            "oswiadczenie_dochodow",
            _L("Oświadczenie o dochodach", "Заявление о доходах", "Income declaration", "Заява про доходи"),
        ),
    ],
    "odwolanie": [
        _doc(
            "odwolanie",
            _L("Szablon odwołania", "Шаблон odwołanie", "Appeal template", "Шаблон odwołanie"),
        ),
        _goto(
            "mos",
            "#mos",
            _L("Wróć do przewodnika MOS", "Вернись к гиду MOS", "Back to MOS guide", "Повернись до гіду MOS"),
        ),
    ],
    "praca": [
        _goto("mos", "#mos", _L("MOS na pracę", "MOS для работы", "MOS for work", "MOS для роботи")),
        _doc(
            "oswiadczenie_dochodow",
            _L("Oświadczenie o dochodach", "Заявление о доходах", "Income declaration", "Заява про доходи"),
        ),
    ],
    "mos": [
        _goto("mos", "#mos", _L("Otwórz przewodnik MOS", "Открыть гид MOS", "Open MOS guide", "Відкрити гід MOS")),
        _doc("pesel", _L("Najpierw PESEL", "Сначала PESEL", "PESEL first", "Спочатку PESEL")),
    ],
    "meldunek": [
        _doc("meldunek", _L("Wypełnij meldunek", "Заполнить meldunek", "Fill meldunek", "Заповнити meldunek")),
        _doc("pesel", _L("Wniosek PESEL", "Заявление PESEL", "PESEL form", "Заява PESEL")),
    ],
}


_TOPICS: dict[str, dict[str, list[str] | dict[str, str]]] = {
    "mos": {
        "keywords": ["mos", "мос", "cudzoziemcy.gov", "wniosek online"],
        "answers": {
            "ru": (
                "<b>MOS 2.0 — официальная подача</b>\n\n"
                "1. Сначала собери PESEL, Profil Zaufany и приложения.\n"
                "2. Отметь checklist готовности в гиде.\n"
                "3. Подай wniosek только на mos.cudzoziemcy.gov.pl.\n\n"
                "Кнопки справа и под ответом откроют нужный шаг — не нужно искать внизу страницы."
            ),
            "en": (
                "<b>MOS 2.0 — official filing</b>\n\n"
                "1. First gather PESEL, trusted profile and attachments.\n"
                "2. Tick the readiness checklist in the guide.\n"
                "3. File only on mos.cudzoziemcy.gov.pl.\n\n"
                "Use the buttons under this answer / in your profile — no need to scroll the whole page."
            ),
            "ua": (
                "<b>MOS 2.0 — офіційна подача</b>\n\n"
                "1. Збери PESEL, Profil Zaufany і додатки.\n"
                "2. Відміть чекліст у гіді.\n"
                "3. Подай тільки на mos.cudzoziemcy.gov.pl."
            ),
            "pl": (
                "<b>MOS 2.0 — oficjalne złożenie</b>\n\n"
                "1. Najpierw zbierz PESEL, Profil Zaufany i załączniki.\n"
                "2. Odznacz checklistę w przewodniku.\n"
                "3. Wniosek złóż tylko na mos.cudzoziemcy.gov.pl.\n\n"
                "Przyciski pod odpowiedzią i w profilu prowadzą dalej — bez szukania na dole strony."
            ),
        },
    },
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
                "2. Основание пребывания: работа, учёба, бизнес или семья.\n"
                "3. Доход, страховка, адрес в Польше.\n"
                "4. Подача — через MOS 2.0 (online).\n\n"
                "Дальше — кнопки: гид MOS или нужный PDF."
            ),
            "en": (
                "<b>Residence card: what to prepare</b>\n\n"
                "1. Passport and copies of relevant pages.\n"
                "2. Basis of stay: work, studies, business, or family.\n"
                "3. Income, insurance, address in Poland.\n"
                "4. File via MOS 2.0 (online).\n\n"
                "Next: use the buttons for the MOS guide or a PDF template."
            ),
            "ua": (
                "<b>Karta pobytu: що підготувати</b>\n\n"
                "1. Паспорт і копії сторінок.\n"
                "2. Підстава перебування, дохід, страховка, адреса.\n"
                "3. Подача через MOS 2.0.\n\n"
                "Далі — кнопки під відповіддю."
            ),
            "pl": (
                "<b>Karta pobytu: co przygotować</b>\n\n"
                "1. Paszport i kopie ważnych stron.\n"
                "2. Podstawa pobytu: praca, studia, firma albo rodzina.\n"
                "3. Dochód, ubezpieczenie, adres w Polsce.\n"
                "4. Złożenie przez MOS 2.0 (online).\n\n"
                "Dalej — przyciski: przewodnik MOS albo PDF."
            ),
        },
    },
    "pesel": {
        "keywords": ["pesel", "песель", "песел"],
        "answers": {
            "ru": (
                "<b>PESEL: коротко</b>\n\n"
                "Обычно нужны: документ личности, адрес в Польше, meldunek или основание для PESEL.\n"
                "Нажми кнопку ниже — откроется форма PDF. Когда заполнишь, отметь шаг в профиле справа."
            ),
            "en": (
                "<b>PESEL: short checklist</b>\n\n"
                "Usually needed: identity document, Polish address, meldunek or legal basis.\n"
                "Use the button below to open the PDF form, then tick the step in your profile."
            ),
            "ua": (
                "<b>PESEL: коротко</b>\n\n"
                "Потрібні: документ особи, адреса в Польщі, meldunek або підстава.\n"
                "Кнопка нижче відкриє PDF; потім відміть крок у профілі справа."
            ),
            "pl": (
                "<b>PESEL: krótka checklista</b>\n\n"
                "Zwykle potrzebne: dokument tożsamości, adres w Polsce, meldunek albo podstawa prawna.\n"
                "Przycisk poniżej otworzy formularz PDF — potem odznacz krok w profilu obok."
            ),
        },
    },
    "meldunek": {
        "keywords": ["meldunek", "zameld", "мельд", "прописк", "address registration"],
        "answers": {
            "ru": (
                "<b>Meldunek</b>\n\n"
                "Нужны: документ личности, основание проживания (umowa najmu и т.п.), адрес.\n"
                "Открой форму кнопкой — после заполнения продолжи checklist MOS в профиле."
            ),
            "en": (
                "<b>Address registration (meldunek)</b>\n\n"
                "Need: ID, proof of housing (e.g. lease), address.\n"
                "Open the form with the button, then continue the MOS checklist in your profile."
            ),
            "ua": (
                "<b>Meldunek</b>\n\n"
                "Потрібні: документ особи, підстава проживання, адреса.\n"
                "Відкрий форму кнопкою і продовж чекліст MOS у профілі."
            ),
            "pl": (
                "<b>Meldunek</b>\n\n"
                "Potrzebne: dokument tożsamości, podstawa zamieszkania (np. umowa), adres.\n"
                "Otwórz formularz przyciskiem — potem kontynuuj checklistę MOS w profilu."
            ),
        },
    },
    "office_letter": {
        "keywords": [
            "письмо",
            "ужонд",
            "urząd",
            "wezwanie",
            "pismo",
            "letter",
            "summons",
        ],
        "answers": {
            "ru": (
                "<b>Письмо из urzędu: что сделать</b>\n\n"
                "1. Найдите срок: часто это 7 или 14 дней.\n"
                "2. Проверьте, что именно требуют.\n"
                "3. Не игнорируйте письмо.\n\n"
                "Ответ на польском — кнопкой ниже (останется в профиле, пока не закончишь)."
            ),
            "en": (
                "<b>Office letter: what to do</b>\n\n"
                "1. Find the deadline (often 7 or 14 days).\n"
                "2. Check what is requested.\n"
                "3. Do not ignore it.\n\n"
                "Draft a Polish reply with the button below — it stays in your profile until done."
            ),
            "ua": (
                "<b>Лист з urzędu</b>\n\n"
                "Знайдіть строк, перевірте вимоги. Відповідь — кнопкою нижче; задача лишиться в профілі."
            ),
            "pl": (
                "<b>Pismo z urzędu: co zrobić</b>\n\n"
                "1. Znajdź termin — często 7 albo 14 dni.\n"
                "2. Sprawdź, czego urząd żąda.\n"
                "3. Nie ignoruj pisma.\n\n"
                "Odpowiedź przygotujesz przyciskiem poniżej — zadanie zostanie w profilu."
            ),
        },
    },
    "upowaznienie": {
        "keywords": [
            "upoważn",
            "pełnomoc",
            "доверен",
            "довірен",
            "power of attorney",
            "authorization",
        ],
        "answers": {
            "ru": (
                "<b>Upoważnienie</b>\n\n"
                "Простой шаблон — кнопкой ниже.\n"
                "Если urząd требует pełnomocnictwo notarialne — этого PDF может не хватить."
            ),
            "en": (
                "<b>Authorization</b>\n\n"
                "Open the simple template with the button below.\n"
                "Some offices require a notarial power of attorney."
            ),
            "ua": "<b>Upoważnienie</b>\n\nШаблон — кнопкою нижче. Нотаріальне може вимагати urząd.",
            "pl": (
                "<b>Upoważnienie</b>\n\n"
                "Szablon otworzysz przyciskiem poniżej.\n"
                "Jeśli urząd wymaga formy notarialnej — ten PDF nie wystarczy."
            ),
        },
    },
    "dochody": {
        "keywords": [
            "dochód",
            "доход",
            "дохід",
            "income",
            "zarob",
            "pensja",
            "зарплат",
        ],
        "answers": {
            "ru": (
                "<b>Oświadczenie o dochodach</b>\n\n"
                "Часто нужно к karcie pobytu: источник, сумма netto, период.\n"
                "Открой шаблон кнопкой — задача появится в профиле справа."
            ),
            "en": (
                "<b>Income declaration</b>\n\n"
                "Often needed for a residence card: source, net amount, period.\n"
                "Open the template with the button — it appears in your profile."
            ),
            "ua": "<b>Заява про доходи</b>\n\nЧасто потрібна до karty. Шаблон — кнопкою; задача в профілі справа.",
            "pl": (
                "<b>Oświadczenie o dochodach</b>\n\n"
                "Często wymagane do karty pobytu: źródło, kwota netto, okres.\n"
                "Szablon otworzysz przyciskiem — zadanie w profilu obok."
            ),
        },
    },
    "zus_nfz": {
        "keywords": ["zus", "nfz", "страх", "ubezpiec", "insurance", "lekarz", "врач"],
        "answers": {
            "ru": (
                "<b>ZUS / NFZ: базово</b>\n\n"
                "При официальной работе работодатель обычно регистрирует в ZUS. "
                "NFZ зависит от действующей страховки.\n\n"
                "Проверьте: umowa, zgłoszenie do ZUS, статус у работодателя или в IKP."
            ),
            "en": (
                "<b>ZUS / NFZ basics</b>\n\n"
                "With legal employment, the employer usually registers you in ZUS. "
                "NFZ access depends on active insurance.\n\n"
                "Check your contract, ZUS registration, or IKP."
            ),
            "ua": (
                "<b>ZUS / NFZ: базово</b>\n\n"
                "При офіційній роботі роботодавець зазвичай реєструє в ZUS. "
                "Доступ до NFZ залежить від активного страхування."
            ),
            "pl": (
                "<b>ZUS / NFZ: podstawy</b>\n\n"
                "Przy legalnej pracy pracodawca zwykle zgłasza Cię do ZUS. "
                "Dostęp do NFZ zależy od aktywnego ubezpieczenia.\n\n"
                "Sprawdź umowę, zgłoszenie ZUS albo IKP."
            ),
        },
    },
    "praca": {
        "keywords": [
            "работа",
            "праця",
            "praca",
            "umowa",
            "work",
            "job",
            "oświadczenie",
        ],
        "answers": {
            "ru": (
                "<b>Работа в Польше: база</b>\n\n"
                "1. Храните umowę и расчётные листки.\n"
                "2. Проверьте zgłoszenie do ZUS.\n"
                "3. Для karty pobytu часто нужны копии договора и доходы.\n\n"
                "Дальше — гид MOS или заявление о доходах (кнопки)."
            ),
            "en": (
                "<b>Work in Poland: basics</b>\n\n"
                "1. Keep your contract and payslips.\n"
                "2. Confirm ZUS registration.\n"
                "3. Residence applications often need contract copies and income proof.\n\n"
                "Next: MOS guide or income declaration (buttons)."
            ),
            "ua": (
                "<b>Робота в Польщі</b>\n\n"
                "Зберігайте umowę і розрахунки, перевірте ZUS. Далі — кнопки MOS або заява про доходи."
            ),
            "pl": (
                "<b>Praca w Polsce: podstawy</b>\n\n"
                "1. Przechowuj umowę i paski.\n"
                "2. Sprawdź zgłoszenie do ZUS.\n"
                "3. Do karty pobytu zwykle potrzebne są kopie umowy i dochody.\n\n"
                "Dalej — przewodnik MOS albo oświadczenie o dochodach."
            ),
        },
    },
    "odwolanie": {
        "keywords": [
            "odwołanie",
            "odwolanie",
            "odmowa",
            "отказ",
            "відмова",
            "appeal",
            "refusal",
            "обжалован",
        ],
        "answers": {
            "ru": (
                "<b>Отказ / odwołanie</b>\n\n"
                "1. Найдите срок обжалования в решении (часто 14 дней).\n"
                "2. Не пропускайте срок.\n"
                "3. Черновик — кнопкой ниже; сложные дела — юрист или urząd (мы не подаём за тебя)."
            ),
            "en": (
                "<b>Refusal / appeal</b>\n\n"
                "1. Find the appeal deadline in the decision (often 14 days).\n"
                "2. Do not miss it.\n"
                "3. Draft with the button below; complex cases → a lawyer or the office (we do not file for you)."
            ),
            "ua": (
                "<b>Відмова / odwołanie</b>\n\n"
                "Перевір строк у рішенні. Чернетка — кнопкою; складні справи — юрист або urząd (ми не подаємо за тебе)."
            ),
            "pl": (
                "<b>Odmowa / odwołanie</b>\n\n"
                "1. Sprawdź termin w decyzji (często 14 dni).\n"
                "2. Nie przegap terminu.\n"
                "3. Szablon przyciskiem poniżej; trudne sprawy — prawnik lub urząd (nie składamy za Ciebie)."
            ),
        },
    },
}

_FALLBACK = {
    "ru": (
        "<b>Я могу помочь с документами в Польше</b>\n\n"
        "Спросите конкретно: PESEL, meldunek, MOS, karta pobytu, ZUS/NFZ или письмо из urzędu.\n"
        "Нужные действия появятся кнопками и в профиле справа — не внизу страницы."
    ),
    "en": (
        "<b>I can help with paperwork in Poland</b>\n\n"
        "Ask about PESEL, meldunek, MOS, residence card, ZUS/NFZ, or office letters.\n"
        "Actions appear as buttons and in your profile beside chat — not at the bottom."
    ),
    "ua": (
        "<b>Можу допомогти з документами в Польщі</b>\n\n"
        "Запитайте про PESEL, meldunek, MOS, kartę pobytu або лист з urzędu.\n"
        "Дії з’являться кнопками і в профілі справа."
    ),
    "pl": (
        "<b>Mogę pomóc z dokumentami w Polsce</b>\n\n"
        "Zapytaj o PESEL, meldunek, MOS, kartę pobytu, ZUS/NFZ albo pismo z urzędu.\n"
        "Akcje pojawią się jako przyciski i w profilu obok czatu — nie na dole strony."
    ),
}


def localize_actions(actions: list[dict] | tuple[dict, ...], lang: str) -> list[dict]:
    safe = lang if lang in {"pl", "ru", "en", "ua"} else "pl"
    out = []
    for raw in actions:
        labels = raw.get("label") or {}
        item = {
            "type": raw["type"],
            "id": raw["id"],
            "label": labels.get(safe) or labels.get("pl") or raw["id"],
        }
        if raw.get("href"):
            item["href"] = raw["href"]
        out.append(item)
    return out


def actions_for_topic(topic: str, lang: str) -> list[dict]:
    return localize_actions(_TOPIC_ACTIONS.get(topic, []), lang)


def answer_question(question: str, lang: str) -> AssistantAnswer:
    normalized = (question or "").casefold()
    safe_lang = lang if lang in ("ru", "en", "ua", "pl") else "ru"

    for topic, data in _TOPICS.items():
        keywords = data["keywords"]
        if any(keyword in normalized for keyword in keywords):
            answers = data["answers"]
            body = answers.get(safe_lang, answers["ru"])
            return AssistantAnswer(
                topic=topic,
                text=f"{body}\n\n{_DISCLAIMER[safe_lang]}",
                actions=tuple(actions_for_topic(topic, safe_lang)),
            )

    return AssistantAnswer(
        topic="fallback",
        text=f"{_FALLBACK[safe_lang]}\n\n{_DISCLAIMER[safe_lang]}",
        actions=tuple(
            localize_actions(
                [
                    _goto("mos", "#mos", _L("Przewodnik MOS", "Гид MOS", "MOS guide", "Гід MOS")),
                    _doc("pesel", _L("PESEL PDF", "PESEL PDF", "PESEL PDF", "PESEL PDF")),
                ],
                safe_lang,
            )
        ),
    )


async def answer_question_smart(question: str, lang: str) -> AssistantAnswer:
    """Rule-based answer first; enrich with knowledge + optional LLM."""
    from src.knowledge import knowledge_context, search_knowledge
    from src.llm import complete_chat

    base = answer_question(question, lang)
    context = knowledge_context(question, lang)
    hits = search_knowledge(question, lang=lang, limit=1)

    system = (
        "You are WniosekPL, a helper for foreigners in Poland. "
        "Give practical next steps. Not legal advice. Use the knowledge context. "
        "Answer in the user's language. Keep under 180 words. Use short bullets. "
        "Do NOT paste document URLs or '/docs → …' paths — the UI shows action buttons."
    )
    user = (
        f"Language: {lang}\nQuestion: {question}\n\n"
        f"Knowledge:\n{context or 'n/a'}\n\n"
        f"Fallback topic: {base.topic}"
    )
    llm_text = await complete_chat(system, user)
    if llm_text:
        topic = hits[0]["id"] if hits else base.topic
        safe_lang = lang if lang in _DISCLAIMER else "ru"
        actions = actions_for_topic(topic, safe_lang) or list(base.actions)
        return AssistantAnswer(
            topic=topic,
            text=f"{llm_text}\n\n{_DISCLAIMER[safe_lang]}",
            actions=tuple(actions),
        )

    if context and base.topic == "fallback" and hits:
        safe_lang = lang if lang in _DISCLAIMER else "ru"
        body = f"<b>{hits[0]['title']}</b>\n\n{hits[0]['body'].strip()}"
        topic = hits[0]["id"]
        return AssistantAnswer(
            topic=topic,
            text=f"{body}\n\n{_DISCLAIMER[safe_lang]}",
            actions=tuple(actions_for_topic(topic, safe_lang) or list(base.actions)),
        )
    return base
