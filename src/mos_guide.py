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


WALKTHROUGH = [
    {
        "id": "pesel_step",
        "pl": "PESEL",
        "ru": "PESEL",
        "en": "PESEL",
        "ua": "PESEL",
        "body_pl": "Jeśli nie masz PESEL — złóż wniosek w gminie albo zamelduj się (często PESEL nadają z urzędu). U nas jest oficjalny PDF PESEL.",
        "body_ru": "Нет PESEL — подай wniosek в gminie или сделай meldunek (часто дают с urzędu). У нас есть официальный PDF PESEL.",
        "body_en": "No PESEL — apply at the commune or register address (often issued automatically). We have the official PESEL PDF.",
        "body_ua": "Немає PESEL — подай wniosek у gminie або зроби meldunek. У нас є офіційний PDF PESEL.",
        "cta_pl": "Wypełnij PESEL",
        "cta_ru": "Заполнить PESEL",
        "cta_en": "Fill PESEL",
        "cta_ua": "Заповнити PESEL",
        "href": "/#documents",
    },
    {
        "id": "pz_step",
        "pl": "Profil Zaufany",
        "ru": "Profil Zaufany",
        "en": "Trusted profile",
        "ua": "Profil Zaufany",
        "body_pl": "Załóż Profil Zaufany (bank / e-dowód / urzędnik). Bez tego nie podpiszesz wniosku w MOS przez login.gov.pl.",
        "body_ru": "Сделай Profil Zaufany (банк / e-dowód / urząd). Без него не подпишешь wniosek в MOS через login.gov.pl.",
        "body_en": "Create a trusted profile (bank / e-ID / office). Without it you cannot sign in MOS via login.gov.pl.",
        "body_ua": "Зроби Profil Zaufany (банк / e-dowód / urząd). Без нього не підпишеш wniosek у MOS.",
        "cta_pl": "Jak założyć PZ",
        "cta_ru": "Как сделать PZ",
        "cta_en": "How to get PZ",
        "cta_ua": "Як зробити PZ",
        "href": "https://www.gov.pl/web/gov/zaloz-profil-zaufany",
    },
    {
        "id": "files_step",
        "pl": "Załączniki",
        "ru": "Приложения",
        "en": "Attachments",
        "ua": "Додатки",
        "body_pl": "Skan całego paszportu, zdjęcie, opłaty, dokumenty celu (praca/studia/rodzina). Przy pracy — email pracodawcy do e-podpisu.",
        "body_ru": "Скан всего паспорта, фото, оплаты, документы цели. При работе — email работодателя для e-подписи.",
        "body_en": "Full passport scan, photo, fees, purpose docs. For work — employer email for e-signature.",
        "body_ua": "Скан усього паспорта, фото, оплати, документи мети. Для роботи — email роботодавця для e-підпису.",
        "cta_pl": "Zobacz listę według celu",
        "cta_ru": "Смотри список по цели",
        "cta_en": "See list by purpose",
        "cta_ua": "Дивись список за метою",
        "href": "#mos-purposes",
    },
    {
        "id": "mos_step",
        "pl": "Konto MOS + wniosek",
        "ru": "Аккаунт MOS + wniosek",
        "en": "MOS account + application",
        "ua": "Акаунт MOS + wniosek",
        "body_pl": "Załóż NOWE konto w MOS (stare nie przeniesiono), zaloguj przez login.gov.pl, wypełnij, dołącz pliki, wyślij — pobierz UPO.",
        "body_ru": "Создай НОВЫЙ аккаунт в MOS (старые не перенесли), войди через login.gov.pl, заполни, приложи файлы, отправь — скачай UPO.",
        "body_en": "Create a NEW MOS account (old ones were not migrated), log in via login.gov.pl, fill, attach, submit — download UPO.",
        "body_ua": "Створи НОВИЙ акаунт у MOS (старі не перенесли), увійди через login.gov.pl, заповни, додай файли, надішли — завантаж UPO.",
        "cta_pl": "Otwórz MOS",
        "cta_ru": "Открыть MOS",
        "cta_en": "Open MOS",
        "cta_ua": "Відкрити MOS",
        "href": MOS_PORTAL_URL,
    },
]

EMPLOYER_HELPER = {
    "pl": {
        "title": "Szablon do pracodawcy / uczelni",
        "body": "Wyślij to osobie, która musi e-podpisać załącznik w MOS:",
        "message": (
            "Dzień dobry,\n\n"
            "Składam wniosek o pobyt przez MOS 2.0 (mos.cudzoziemcy.gov.pl). "
            "System wyśle Państwu link e-mail z załącznikiem do wypełnienia i podpisu elektronicznego "
            "(Profil Zaufany / podpis kwalifikowany). Proszę o szybkie podpisanie — bez tego nie złożę wniosku.\n\n"
            "Dziękuję!"
        ),
    },
    "ru": {
        "title": "Текст для работодателя / вуза",
        "body": "Отправь человеку, который должен e-подписать załącznik в MOS:",
        "message": (
            "Добрый день,\n\n"
            "Подаю заявление о pobyt через MOS 2.0 (mos.cudzoziemcy.gov.pl). "
            "Система пришлёт вам email со ссылкой на załącznik для заполнения и электронной подписи "
            "(Profil Zaufany / квалифицированная подпись). Пожалуйста, подпишите быстрее — без этого я не подам wniosek.\n\n"
            "Спасибо!"
        ),
    },
    "en": {
        "title": "Message for employer / university",
        "body": "Send this to the person who must e-sign the MOS attachment:",
        "message": (
            "Hello,\n\n"
            "I am filing a residence application via MOS 2.0 (mos.cudzoziemcy.gov.pl). "
            "The system will email you a link to complete and electronically sign an attachment "
            "(trusted profile / qualified signature). Please sign quickly — I cannot submit without it.\n\n"
            "Thank you!"
        ),
    },
    "ua": {
        "title": "Текст для роботодавця / вишу",
        "body": "Надішли людині, яка має e-підписати załącznik у MOS:",
        "message": (
            "Добрий день,\n\n"
            "Подаю заяву про pobyt через MOS 2.0 (mos.cudzoziemcy.gov.pl). "
            "Система надішле вам email з лінком на załącznik для заповнення та електронного підпису "
            "(Profil Zaufany / кваліфікований підпис). Прошу підписати швидко — без цього не подам wniosek.\n\n"
            "Дякую!"
        ),
    },
}


def next_action(done: dict[str, bool] | None, lang: str = "pl") -> dict:
    """Return the first incomplete readiness step as the next action."""
    lang = lang if lang in {"pl", "ru", "en", "ua"} else "pl"
    state = done or {}
    for step in READY_STEPS:
        if not state.get(step["id"]):
            return {
                "id": step["id"],
                "title": step.get(lang, step["pl"]),
                "hint": step.get(f"hint_{lang}", step["hint_pl"]),
                "link": step.get("link") or "#mos",
                "done_count": sum(1 for s in READY_STEPS if state.get(s["id"])),
                "total": len(READY_STEPS),
                "complete": False,
            }
    return {
        "id": "open_mos",
        "title": {
            "pl": "Wszystko gotowe — otwórz MOS i złóż wniosek",
            "ru": "Всё готово — открой MOS и подай wniosek",
            "en": "All set — open MOS and file",
            "ua": "Усе готово — відкрий MOS і подай wniosek",
        }[lang],
        "hint": {
            "pl": "Załóż nowe konto, zaloguj login.gov.pl, dołącz pliki i pobierz UPO.",
            "ru": "Создай новый аккаунт, войди login.gov.pl, приложи файлы и скачай UPO.",
            "en": "Create a new account, log in via login.gov.pl, attach files, download UPO.",
            "ua": "Створи новий акаунт, увійди login.gov.pl, додай файли і завантаж UPO.",
        }[lang],
        "link": MOS_PORTAL_URL,
        "done_count": len(READY_STEPS),
        "total": len(READY_STEPS),
        "complete": True,
    }


def guide_payload(lang: str = "pl", done: dict[str, bool] | None = None) -> dict:
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
            "sub": "Jeden następny krok naraz. Potem oficjalny wniosek na mos.cudzoziemcy.gov.pl.",
            "cta": "Otwórz MOS",
            "info": "Info UdSC",
            "ready_title": "Checklist gotowości",
            "purpose_title": "Wybierz cel pobytu — pokażemy typowe załączniki.",
            "walk_title": "Ścieżka przewodnika",
            "next_title": "Twój następny krok",
            "next_done": "Wszystko gotowe",
            "do_step": "Zrób ten krok",
            "mark_done": "Mam to — dalej",
            "open_mos_btn": "Otwórz MOS i złóż",
            "tab_purpose": "Załączniki",
            "tab_employer": "Do pracodawcy",
            "tab_deadline": "Termin pobytu",
            "deadline_title": "Koniec legalnego pobytu",
            "deadline_btn": "Dodaj przypomnienie",
            "deadline_hint": "Podaj datę — zapiszemy termin i przypomnimy ~14 dni wcześniej (po zalogowaniu).",
            "deadline_calendar": "Kalendarz konta",
            "deadline_ok": "Zapisano termin + przypomnienie. Punkt „legalny pobyt” odznaczony.",
            "deadline_login": "Zaloguj się (prawy górny róg), żeby zapisać przypomnienie.",
            "copy_employer": "Kopiuj wiadomość",
            "copied": "Skopiowano",
            "sync_account": "Postęp zapisany na koncie.",
            "sync_local": "Postęp zapisany na tym urządzeniu. Zaloguj się, żeby przenieść na inne.",
            "disclaimer": "WniosekPL nie jest urzędem i nie składa wniosku za Ciebie. Od 27.04.2026 pobyt czasowy/stały/rezydent UE — zasadniczo tylko online w MOS.",
            "open_mos": "Przejdź do mos.cudzoziemcy.gov.pl",
        },
        "ru": {
            "title": "Подготовка к MOS 2.0",
            "sub": "Один следующий шаг за раз. Потом официальный wniosek на mos.cudzoziemcy.gov.pl.",
            "cta": "Открыть MOS",
            "info": "Info UdSC",
            "ready_title": "Чеклист готовности",
            "purpose_title": "Выбери цель pobytu — покажем типичные приложения.",
            "walk_title": "Путь проводника",
            "next_title": "Твой следующий шаг",
            "next_done": "Всё готово",
            "do_step": "Сделать этот шаг",
            "mark_done": "Готово — дальше",
            "open_mos_btn": "Открыть MOS и подать",
            "tab_purpose": "Приложения",
            "tab_employer": "Работодателю",
            "tab_deadline": "Срок pobytu",
            "deadline_title": "Конец легального pobytu",
            "deadline_btn": "Добавить напоминание",
            "deadline_hint": "Укажи дату — сохраним срок и напомним ~за 14 дней (после входа).",
            "deadline_calendar": "Календарь аккаунта",
            "deadline_ok": "Срок и напоминание сохранены. Пункт «легальный pobyt» отмечен.",
            "deadline_login": "Войди (справа сверху), чтобы сохранить напоминание.",
            "copy_employer": "Скопировать текст",
            "copied": "Скопировано",
            "sync_account": "Прогресс сохранён в аккаунте.",
            "sync_local": "Прогресс на этом устройстве. Войди, чтобы перенести на другое.",
            "disclaimer": "WniosekPL — не urząd и не подаёт заявление за тебя. С 27.04.2026 pobyt — в основном только online в MOS.",
            "open_mos": "Перейти на mos.cudzoziemcy.gov.pl",
        },
        "en": {
            "title": "Prepare for MOS 2.0",
            "sub": "One next step at a time. Then file on mos.cudzoziemcy.gov.pl.",
            "cta": "Open MOS",
            "info": "UdSC info",
            "ready_title": "Readiness checklist",
            "purpose_title": "Pick your purpose of stay — we show typical attachments.",
            "walk_title": "Guide path",
            "next_title": "Your next step",
            "next_done": "You are ready",
            "do_step": "Do this step",
            "mark_done": "Done — next",
            "open_mos_btn": "Open MOS and file",
            "tab_purpose": "Attachments",
            "tab_employer": "For employer",
            "tab_deadline": "Stay deadline",
            "deadline_title": "Legal stay end date",
            "deadline_btn": "Add reminder",
            "deadline_hint": "Enter the date — we save it and remind ~14 days earlier (after login).",
            "deadline_calendar": "Account calendar",
            "deadline_ok": "Deadline + reminder saved. “Legal stay” step marked done.",
            "deadline_login": "Log in (top right) to save the reminder.",
            "copy_employer": "Copy message",
            "copied": "Copied",
            "sync_account": "Progress saved to your account.",
            "sync_local": "Saved on this device. Log in to sync elsewhere.",
            "disclaimer": "WniosekPL is not a government office and does not file for you. Since 27 Apr 2026 residence permits are mostly online-only via MOS.",
            "open_mos": "Go to mos.cudzoziemcy.gov.pl",
        },
        "ua": {
            "title": "Підготовка до MOS 2.0",
            "sub": "Один наступний крок за раз. Потім офіційний wniosek на mos.cudzoziemcy.gov.pl.",
            "cta": "Відкрити MOS",
            "info": "Info UdSC",
            "ready_title": "Чекліст готовності",
            "purpose_title": "Обери мету pobytu — покажемо типові додатки.",
            "walk_title": "Шлях провідника",
            "next_title": "Твій наступний крок",
            "next_done": "Усе готово",
            "do_step": "Зробити цей крок",
            "mark_done": "Є — далі",
            "open_mos_btn": "Відкрити MOS і подати",
            "tab_purpose": "Додатки",
            "tab_employer": "Роботодавцю",
            "tab_deadline": "Термін pobytu",
            "deadline_title": "Кінець легального pobytu",
            "deadline_btn": "Додати нагадування",
            "deadline_hint": "Вкажи дату — збережемо строк і нагадаємо ~за 14 днів (після входу).",
            "deadline_calendar": "Календар акаунта",
            "deadline_ok": "Строк і нагадування збережено. Пункт «легальний pobyt» відмічено.",
            "deadline_login": "Увійди (справа зверху), щоб зберегти нагадування.",
            "copy_employer": "Скопіювати текст",
            "copied": "Скопійовано",
            "sync_account": "Прогрес збережено в акаунті.",
            "sync_local": "Збережено на цьому пристрої. Увійди, щоб синхронізувати.",
            "disclaimer": "WniosekPL — не urząd і не подає заяву за тебе. З 27.04.2026 pobyt здебільшого тільки online в MOS.",
            "open_mos": "Перейти на mos.cudzoziemcy.gov.pl",
        },
    }

    walkthrough = []
    for step in WALKTHROUGH:
        walkthrough.append(
            {
                "id": step["id"],
                "title": step.get(lang, step["pl"]),
                "body": step.get(f"body_{lang}", step["body_pl"]),
                "cta": step.get(f"cta_{lang}", step["cta_pl"]),
                "href": step.get("href"),
            }
        )

    return {
        "portal_url": MOS_PORTAL_URL,
        "info_url": MOS_INFO_URL,
        "lang": lang,
        "copy": headlines[lang],
        "journey": journey,
        "ready": ready,
        "purposes": purposes,
        "walkthrough": walkthrough,
        "employer_helper": EMPLOYER_HELPER[lang],
        "next_action": next_action(done, lang),
    }
