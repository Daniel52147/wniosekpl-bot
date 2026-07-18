"""MOS 2.0 guide — prepare foreigners before official online filing."""

from __future__ import annotations

MOS_PORTAL_URL = "https://mos.cudzoziemcy.gov.pl"
MOS_INFO_URL = "https://www.gov.pl/web/udsc/info-mos"

# Readiness gates before logging into MOS
READY_STEPS = [
    {
        "id": "pesel",
        "pl": "Mam numer PESEL",
        "ru": "У меня есть PESEL",
        "en": "I have a PESEL number",
        "ua": "Маю номер PESEL",
        "hint_pl": "Bez PESEL trudno założyć Profil Zaufany i wejść do MOS.",
        "hint_ru": "Без PESEL сложно сделать Profil Zaufany и войти в MOS.",
        "hint_en": "Without PESEL it is hard to get a trusted profile and enter MOS.",
        "hint_ua": "Без PESEL важко зробити Profil Zaufany і увійти в MOS.",
        "link": "/#documents",
    },
    {
        "id": "trusted_profile",
        "pl": "Mam Profil Zaufany / login.gov.pl",
        "ru": "Есть Profil Zaufany / login.gov.pl",
        "en": "I have a trusted profile / login.gov.pl",
        "ua": "Є Profil Zaufany / login.gov.pl",
        "hint_pl": "MOS loguje przez login.gov.pl — potrzebujesz podpisu elektronicznego.",
        "hint_ru": "MOS входит через login.gov.pl — нужна электронная подпись.",
        "hint_en": "MOS logs in via login.gov.pl — you need an electronic signature.",
        "hint_ua": "MOS входить через login.gov.pl — потрібен електронний підпис.",
        "link": "https://www.gov.pl/web/gov/zaloz-profil-zaufany",
    },
    {
        "id": "legal_stay",
        "pl": "Wiem, do kiedy mam legalny pobyt",
        "ru": "Знаю, до какой даты легальный pobyt",
        "en": "I know when my legal stay ends",
        "ua": "Знаю, до якої дати легальний pobyt",
        "hint_pl": "Nie czekaj na ostatni dzień — załączniki od pracodawcy mogą potrwać.",
        "hint_ru": "Не жди последний день — załącznik от работодателя может занять время.",
        "hint_en": "Do not wait until the last day — employer attachments can take time.",
        "hint_ua": "Не чекай останній день — załącznik від роботодавця може зайняти час.",
        "link": "/#assistant",
    },
    {
        "id": "passport_scan",
        "pl": "Mam skan / zdjęcia wszystkich stron paszportu",
        "ru": "Есть скан / фото всех страниц паспорта",
        "en": "I have scans/photos of all passport pages",
        "ua": "Є скан / фото всіх сторінок паспорта",
        "hint_pl": "MOS wymaga odwzorowania cyfrowego całego dokumentu podróży.",
        "hint_ru": "MOS требует цифровые копии всего проездного документа.",
        "hint_en": "MOS requires a digital copy of the full travel document.",
        "hint_ua": "MOS вимагає цифрових копій усього проїзного документа.",
        "link": "#mos",
    },
    {
        "id": "photo",
        "pl": "Mam aktualne zdjęcie cyfrowe do wniosku",
        "ru": "Есть актуальное цифровое фото",
        "en": "I have a current digital photo",
        "ua": "Є актуальне цифрове фото",
        "hint_pl": "Przygotuj zdjęcie zgodne z wymaganiami urzędu (format cyfrowy).",
        "hint_ru": "Подготовь фото по требованиям urzędu (цифровой формат).",
        "hint_en": "Prepare a photo matching office requirements (digital).",
        "hint_ua": "Підготуй фото за вимогами urzędu (цифровий формат).",
        "link": "#mos",
    },
    {
        "id": "fees",
        "pl": "Wiem o opłacie skarbowej + 100 zł za kartę",
        "ru": "Знаю про opłatę skarbową + 100 zł за kartę",
        "en": "I know about stamp duty + 100 zł card fee",
        "ua": "Знаю про opłatę skarbową + 100 zł за kartę",
        "hint_pl": "Opłata skarbowa zwykle 340–640 zł zależnie od typu zezwolenia + 100 zł karta.",
        "hint_ru": "Пошлина обычно 340–640 zł в зависимости от типа + 100 zł карта.",
        "hint_en": "Stamp duty is usually 340–640 zł depending on permit type + 100 zł card.",
        "hint_ua": "Збір зазвичай 340–640 zł залежно від типу + 100 zł карта.",
        "link": "#mos",
    },
    {
        "id": "employer_ready",
        "pl": "Jeśli praca/studia — wiem, kto podpisze załącznik e-mailem",
        "ru": "Если работа/учёба — знаю, кто подпишет załącznik по email",
        "en": "If work/studies — I know who will e-sign the attachment",
        "ua": "Якщо робота/навчання — знаю, хто підпише załącznik emailом",
        "hint_pl": "MOS wyśle link do pracodawcy/uczelni — bez ich e-podpisu wniosek nie przejdzie.",
        "hint_ru": "MOS отправит ссылку работодателю/вузу — без их e-подписи не подашь.",
        "hint_en": "MOS emails a link to employer/university — without their e-signature you cannot finish.",
        "hint_ua": "MOS надішле лінк роботодавцю/вишу — без їх e-підпису не подаси.",
        "link": "#mos",
    },
]

JOURNEY = [
    {
        "id": "1",
        "pl": "Zbierz PESEL i Profil Zaufany",
        "ru": "Собери PESEL и Profil Zaufany",
        "en": "Get PESEL and a trusted profile",
        "ua": "Збери PESEL і Profil Zaufany",
    },
    {
        "id": "2",
        "pl": "Odznacz checklistę gotowości poniżej",
        "ru": "Отметь чеклист готовности ниже",
        "en": "Tick the readiness checklist below",
        "ua": "Відміть чекліст готовності нижче",
    },
    {
        "id": "3",
        "pl": "Przygotuj załączniki pod swój cel pobytu",
        "ru": "Подготовь приложения под свою цель pobytu",
        "en": "Prepare attachments for your purpose of stay",
        "ua": "Підготуй додатки під свою мету pobytu",
    },
    {
        "id": "4",
        "pl": "Załóż konto w MOS i złóż wniosek online",
        "ru": "Создай аккаунт в MOS и подай online",
        "en": "Create a MOS account and file online",
        "ua": "Створи акаунт у MOS і подай online",
    },
]

PURPOSES = [
    {
        "id": "work",
        "pl": "Praca",
        "ru": "Работа",
        "en": "Work",
        "ua": "Робота",
        "items_pl": [
            "Umowa / warunki pracy",
            "Email pracodawcy do e-podpisu załącznika w MOS",
            "Potwierdzenie opłat",
            "Skan paszportu + zdjęcie",
        ],
        "items_ru": [
            "Договор / условия работы",
            "Email работодателя для e-подписи в MOS",
            "Подтверждение оплаты",
            "Скан паспорта + фото",
        ],
        "items_en": [
            "Employment contract / work conditions",
            "Employer email for MOS e-signature",
            "Proof of payment",
            "Passport scan + photo",
        ],
        "items_ua": [
            "Договір / умови роботи",
            "Email роботодавця для e-підпису в MOS",
            "Підтвердження оплати",
            "Скан паспорта + фото",
        ],
    },
    {
        "id": "study",
        "pl": "Studia",
        "ru": "Учёба",
        "en": "Studies",
        "ua": "Навчання",
        "items_pl": [
            "Zaświadczenie z uczelni",
            "Email jednostki prowadzącej studia (e-podpis)",
            "Ubezpieczenie",
            "Środki na utrzymanie",
        ],
        "items_ru": [
            "Справка из вуза",
            "Email учебного заведения (e-подпись)",
            "Страховка",
            "Средства на жизнь",
        ],
        "items_en": [
            "University certificate",
            "University email (e-signature)",
            "Insurance",
            "Means of subsistence",
        ],
        "items_ua": [
            "Довідка з вишу",
            "Email навчального закладу (e-підпис)",
            "Страхування",
            "Кошти на життя",
        ],
    },
    {
        "id": "family",
        "pl": "Rodzina",
        "ru": "Семья",
        "en": "Family",
        "ua": "Сім'я",
        "items_pl": [
            "Akty stanu cywilnego / pokrewieństwa",
            "Dokumenty członka rodziny w PL",
            "Adres i ubezpieczenie",
            "Uwaga: część spraw rodzinnych nadal papierowo — sprawdź wyjątki UdSC",
        ],
        "items_ru": [
            "Акты гражданского состояния / родства",
            "Документы члена семьи в PL",
            "Адрес и страховка",
            "Внимание: часть семейных дел всё ещё бумажно — проверь исключения UdSC",
        ],
        "items_en": [
            "Civil status / family documents",
            "Documents of family member in PL",
            "Address and insurance",
            "Note: some family cases still paper — check UdSC exceptions",
        ],
        "items_ua": [
            "Акти цивільного стану / спорідненості",
            "Документи члена сім'ї в PL",
            "Адреса і страхування",
            "Увага: частина сімейних справ ще паперові — перевір винятки UdSC",
        ],
    },
    {
        "id": "business",
        "pl": "Biznes",
        "ru": "Бизнес",
        "en": "Business",
        "ua": "Бізнес",
        "items_pl": [
            "Dokumenty spółki / CEIDG",
            "Załącznik e-podpisany (zarząd / prokura) jeśli wymagany",
            "Dochody / środki",
            "Adres działalności",
        ],
        "items_ru": [
            "Документы компании / CEIDG",
            "E-подписанный załącznik (zarząd / prokura) если нужен",
            "Доходы / средства",
            "Адрес деятельности",
        ],
        "items_en": [
            "Company / CEIDG documents",
            "E-signed attachment (board/proxy) if required",
            "Income / funds",
            "Business address",
        ],
        "items_ua": [
            "Документи компанії / CEIDG",
            "E-підписаний załącznik (zarząd / prokura) якщо треба",
            "Доходи / кошти",
            "Адреса діяльності",
        ],
    },
]


def _pick(row: dict, lang: str, key: str, fallback: str = "pl") -> str:
    return row.get(f"{key}_{lang}") or row.get(lang) or row.get(f"{key}_{fallback}") or row.get(fallback) or ""


def guide_payload(lang: str = "pl") -> dict:
    lang = (lang or "pl").lower()
    if lang not in {"pl", "ru", "en", "ua"}:
        lang = "pl"

    ready = []
    for step in READY_STEPS:
        ready.append(
            {
                "id": step["id"],
                "title": step.get(lang, step["pl"]),
                "hint": step.get(f"hint_{lang}", step["hint_pl"]),
                "link": step.get("link"),
            }
        )

    journey = [
        {"id": s["id"], "title": s.get(lang, s["pl"])}
        for s in JOURNEY
    ]

    purposes = []
    for p in PURPOSES:
        items_key = f"items_{lang}"
        purposes.append(
            {
                "id": p["id"],
                "title": p.get(lang, p["pl"]),
                "items": p.get(items_key, p["items_pl"]),
            }
        )

    headlines = {
        "pl": {
            "title": "Przygotowanie do MOS 2.0",
            "sub": "Oficjalny wniosek o pobyt składasz w portalu państwa. My przeprowadzimy Cię krok po kroku — zanim się zalogujesz.",
            "cta": "Otwórz oficjalny MOS",
            "info": "Informacja UdSC o MOS",
            "ready_title": "Czy jesteś gotowy?",
            "purpose_title": "Załączniki według celu",
            "disclaimer": "WniosekPL nie jest urzędem i nie składa wniosku za Ciebie. Od 27.04.2026 pobyt czasowy/stały/rezydent UE — zasadniczo tylko online w MOS.",
            "open_mos": "Przejdź do mos.cudzoziemcy.gov.pl",
        },
        "ru": {
            "title": "Подготовка к MOS 2.0",
            "sub": "Официальный wniosek о pobyt подаёшь на гос.портале. Мы проведём тебя шаг за шагом — до входа в систему.",
            "cta": "Открыть официальный MOS",
            "info": "Информация UdSC о MOS",
            "ready_title": "Ты готов?",
            "purpose_title": "Приложения по цели",
            "disclaimer": "WniosekPL — не urząd и не подаёт заявление за тебя. С 27.04.2026 pobyt — в основном только online в MOS.",
            "open_mos": "Перейти на mos.cudzoziemcy.gov.pl",
        },
        "en": {
            "title": "Prepare for MOS 2.0",
            "sub": "You file the official residence application on the government portal. We guide you step by step — before you log in.",
            "cta": "Open official MOS",
            "info": "UdSC information about MOS",
            "ready_title": "Are you ready?",
            "purpose_title": "Attachments by purpose",
            "disclaimer": "WniosekPL is not a government office and does not file for you. Since 27 Apr 2026 residence permits are mostly online-only via MOS.",
            "open_mos": "Go to mos.cudzoziemcy.gov.pl",
        },
        "ua": {
            "title": "Підготовка до MOS 2.0",
            "sub": "Офіційний wniosek про pobyt подаєш на держпорталі. Ми проведемо крок за кроком — до входу в систему.",
            "cta": "Відкрити офіційний MOS",
            "info": "Інформація UdSC про MOS",
            "ready_title": "Чи готовий ти?",
            "purpose_title": "Додатки за метою",
            "disclaimer": "WniosekPL — не urząd і не подає заяву за тебе. З 27.04.2026 pobyt здебільшого тільки online в MOS.",
            "open_mos": "Перейти на mos.cudzoziemcy.gov.pl",
        },
    }

    return {
        "portal_url": MOS_PORTAL_URL,
        "info_url": MOS_INFO_URL,
        "lang": lang,
        "copy": headlines[lang],
        "journey": journey,
        "ready": ready,
        "purposes": purposes,
    }
