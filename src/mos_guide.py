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
        "action_pl": "Zrób PESEL (albo meldunek)",
        "action_ru": "Сделай PESEL (или регистрацию адреса — meldunek)",
        "action_en": "Get a PESEL (or address registration)",
        "action_ua": "Зроби PESEL (або реєстрацію адреси — meldunek)",
        "hint_pl": "Bez PESEL trudno założyć Profil Zaufany i wejść do MOS. U nas jest PDF wniosku.",
        "hint_ru": "Без PESEL сложно сделать Profil Zaufany и войти в MOS. У нас есть PDF заявления.",
        "hint_en": "Without PESEL it is hard to get a trusted profile and enter MOS. We have the PDF form.",
        "hint_ua": "Без PESEL важко зробити Profil Zaufany і увійти в MOS. У нас є PDF заяви.",
        "time_pl": "~1 wizyta w urzędzie / gminie",
        "time_ru": "~1 визит в ужонд / гміну",
        "time_en": "~1 visit to the commune office",
        "time_ua": "~1 візит до ужонду / гміни",
        "link": "/profile?tab=docs",
        "doc_id": "pesel",
    },
    {
        "id": "trusted_profile",
        "pl": "Mam Profil Zaufany / login.gov.pl",
        "ru": "Есть Profil Zaufany / login.gov.pl",
        "en": "I have a trusted profile / login.gov.pl",
        "ua": "Є Profil Zaufany / login.gov.pl",
        "action_pl": "Załóż Profil Zaufany (bank / e-dowód)",
        "action_ru": "Сделай Profil Zaufany (банк / e-dowód)",
        "action_en": "Create a trusted profile (bank / e-ID)",
        "action_ua": "Зроби Profil Zaufany (банк / e-dowód)",
        "hint_pl": "MOS loguje przez login.gov.pl — bez tego nie podpiszesz wniosku.",
        "hint_ru": "MOS входит через login.gov.pl — без этого не подпишешь заявление.",
        "hint_en": "MOS logs in via login.gov.pl — without it you cannot sign.",
        "hint_ua": "MOS входить через login.gov.pl — без цього не підпишеш заяву.",
        "time_pl": "ok. 15–30 min online",
        "time_ru": "ок. 15–30 мин online",
        "time_en": "about 15–30 min online",
        "time_ua": "бл. 15–30 хв online",
        "link": "https://www.gov.pl/web/gov/zaloz-profil-zaufany",
    },
    {
        "id": "legal_stay",
        "pl": "Wiem, do kiedy mam legalny pobyt",
        "ru": "Знаю, до какой даты легальное пребывание (pobyt)",
        "en": "I know when my legal stay ends",
        "ua": "Знаю, до якої дати легальне перебування (pobyt)",
        "action_pl": "Zapisz datę końca legalnego pobytu",
        "action_ru": "Запиши дату конца легального пребывания",
        "action_en": "Save your legal stay end date",
        "action_ua": "Запиши дату кінця легального перебування",
        "hint_pl": "Nie czekaj na ostatni dzień — załączniki od pracodawcy mogą potrwać.",
        "hint_ru": "Не жди последний день — приложение от работодателя может занять время.",
        "hint_en": "Do not wait until the last day — employer attachments can take time.",
        "hint_ua": "Не чекай останній день — додаток від роботодавця може зайняти час.",
        "time_pl": "1 minuta",
        "time_ru": "1 минута",
        "time_en": "1 minute",
        "time_ua": "1 хвилина",
        "link": "#mos-deadline-date",
    },
    {
        "id": "passport_scan",
        "pl": "Mam skan / zdjęcia wszystkich stron paszportu",
        "ru": "Есть скан / фото всех страниц паспорта",
        "en": "I have scans/photos of all passport pages",
        "ua": "Є скан / фото всіх сторінок паспорта",
        "action_pl": "Zrób skan całego paszportu (wszystkie strony)",
        "action_ru": "Сделай скан всего паспорта (все страницы)",
        "action_en": "Scan the full passport (all pages)",
        "action_ua": "Зроби скан усього паспорта (усі сторінки)",
        "hint_pl": "MOS wymaga cyfrowej kopii całego dokumentu podróży — nie tylko strony ze zdjęciem.",
        "hint_ru": "MOS требует цифровые копии всего проездного — не только страницу с фото.",
        "hint_en": "MOS needs a digital copy of the full travel document — not just the photo page.",
        "hint_ua": "MOS потребує цифрової копії всього документа — не лише сторінки з фото.",
        "time_pl": "10–20 min",
        "time_ru": "10–20 мин",
        "time_en": "10–20 min",
        "time_ua": "10–20 хв",
        "link": "#mos-ready",
    },
    {
        "id": "photo",
        "pl": "Mam aktualne zdjęcie cyfrowe do wniosku",
        "ru": "Есть актуальное цифровое фото",
        "en": "I have a current digital photo",
        "ua": "Є актуальне цифрове фото",
        "action_pl": "Przygotuj aktualne zdjęcie cyfrowe",
        "action_ru": "Подготовь актуальное цифровое фото",
        "action_en": "Prepare a current digital photo",
        "action_ua": "Підготуй актуальне цифрове фото",
        "hint_pl": "Zdjęcie w formacie cyfrowym, zgodne z wymaganiami urzędu.",
        "hint_ru": "Фото в цифровом формате по требованиям ужонда.",
        "hint_en": "A digital photo matching office requirements.",
        "hint_ua": "Фото в цифровому форматі за вимогами ужонду.",
        "time_pl": "ok. 1 dzień (punkt foto)",
        "time_ru": "ок. 1 день (фотопункт)",
        "time_en": "about 1 day (photo shop)",
        "time_ua": "бл. 1 день (фотопункт)",
        "link": "#mos-ready",
    },
    {
        "id": "fees",
        "pl": "Wiem o opłacie skarbowej + 100 zł za kartę",
        "ru": "Знаю про госпошлину (opłata skarbowa) + 100 zł за карту",
        "en": "I know about stamp duty + 100 zł card fee",
        "ua": "Знаю про держзбір (opłata skarbowa) + 100 zł за карту",
        "action_pl": "Sprawdź opłaty (skarbowa + 100 zł karta)",
        "action_ru": "Проверь пошлины (госпошлина + 100 zł карта)",
        "action_en": "Check the fees (stamp duty + 100 zł card)",
        "action_ua": "Перевір збори (держзбір + 100 zł карта)",
        "hint_pl": "Opłata skarbowa zwykle 340–640 zł zależnie od typu zezwolenia + 100 zł za kartę.",
        "hint_ru": "Пошлина обычно 340–640 zł в зависимости от типа + 100 zł за карту.",
        "hint_en": "Stamp duty is usually 340–640 zł depending on permit type + 100 zł card.",
        "hint_ua": "Збір зазвичай 340–640 zł залежно від типу + 100 zł за карту.",
        "time_pl": "5 min",
        "time_ru": "5 мин",
        "time_en": "5 min",
        "time_ua": "5 хв",
        "link": "#mos-ready",
    },
    {
        "id": "employer_ready",
        "pl": "Jeśli praca/studia — wiem, kto podpisze załącznik e-mailem",
        "ru": "Если работа/учёба — знаю, кто подпишет приложение по email",
        "en": "If work/studies — I know who will e-sign the attachment",
        "ua": "Якщо робота/навчання — знаю, хто підпише додаток emailом",
        "action_pl": "Ustal, kto e-podpisze załącznik (email)",
        "action_ru": "Узнай, кто e-подпишет приложение (email)",
        "action_en": "Confirm who will e-sign the attachment (email)",
        "action_ua": "Дізнайся, хто e-підпише додаток (email)",
        "hint_pl": "MOS wyśle link do pracodawcy/uczelni — bez ich e-podpisu wniosek nie przejdzie. Skopiuj szablon wiadomości.",
        "hint_ru": "MOS отправит ссылку работодателю/вузу — без их e-подписи не подашь. Скопируй шаблон письма.",
        "hint_en": "MOS emails a link to employer/university — without their e-signature you cannot finish. Copy the message template.",
        "hint_ua": "MOS надішле лінк роботодавцю/вишу — без їх e-підпису не подаси. Скопіюй шаблон листа.",
        "time_pl": "napisz dziś / jutro",
        "time_ru": "напиши сегодня / завтра",
        "time_en": "write today / tomorrow",
        "time_ua": "напиши сьогодні / завтра",
        "link": "#mos-helpers",
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
        "ru": "Подготовь приложения под свою цель пребывания",
        "en": "Prepare attachments for your purpose of stay",
        "ua": "Підготуй додатки під свою мету перебування",
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
            "E-подписанный приложение (zarząd / prokura) если нужен",
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
            "E-підписаний додаток (zarząd / prokura) якщо треба",
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
        "body_ru": "Нет PESEL — подай заявление в гмине или сделай регистрацию адреса (meldunek; часто дают с ужонда). У нас есть официальный PDF PESEL.",
        "body_en": "No PESEL — apply at the commune or register address (often issued automatically). We have the official PESEL PDF.",
        "body_ua": "Немає PESEL — подай заяву в гміні або зроби реєстрацію адреси (meldunek). У нас є офіційний PDF PESEL.",
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
        "body_ru": "Сделай Profil Zaufany (банк / e-dowód / ужонд). Без него не подпишешь заявление в MOS через login.gov.pl.",
        "body_en": "Create a trusted profile (bank / e-ID / office). Without it you cannot sign in MOS via login.gov.pl.",
        "body_ua": "Зроби Profil Zaufany (банк / e-dowód / ужонд). Без нього не підпишеш заяву у MOS.",
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
        "ru": "Аккаунт MOS + заявление",
        "en": "MOS account + application",
        "ua": "Акаунт MOS + заява",
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
        "body": "Отправь человеку, который должен e-подписать приложение в MOS:",
        "message": (
            "Добрый день,\n\n"
            "Подаю заявление о пребывании (pobyt) через MOS 2.0 (mos.cudzoziemcy.gov.pl). "
            "Система пришлёт вам email со ссылкой на приложение для заполнения и электронной подписи "
            "(Profil Zaufany / квалифицированная подпись). Пожалуйста, подпишите быстрее — без этого я не подам заявление.\n\n"
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
        "body": "Надішли людині, яка має e-підписати додаток у MOS:",
        "message": (
            "Добрий день,\n\n"
            "Подаю заяву про перебування (pobyt) через MOS 2.0 (mos.cudzoziemcy.gov.pl). "
            "Система надішле вам email з лінком на додаток для заповнення та електронного підпису "
            "(Profil Zaufany / кваліфікований підпис). Прошу підписати швидко — без цього не подам заяву.\n\n"
            "Дякую!"
        ),
    },
}


# What to do inside the official MOS portal after checklist is done
MOS_FILING_STEPS = [
    {
        "id": "login",
        "pl": "Zaloguj się do MOS przez login.gov.pl (Profil Zaufany)",
        "ru": "Войди в MOS через login.gov.pl (Profil Zaufany)",
        "en": "Log into MOS via login.gov.pl (trusted profile)",
        "ua": "Увійди в MOS через login.gov.pl (Profil Zaufany)",
    },
    {
        "id": "wniosek",
        "pl": "Utwórz nowy wniosek o pobyt i wypełnij dane",
        "ru": "Создай новое заявление о пребывании и заполни данные",
        "en": "Create a new residence application and fill in your data",
        "ua": "Створи нову заяву про перебування і заповни дані",
    },
    {
        "id": "pliki",
        "pl": "Dołącz pliki: paszport, zdjęcie, opłaty, dokumenty celu",
        "ru": "Приложи файлы: паспорт, фото, оплаты, документы цели",
        "en": "Attach files: passport, photo, fees, purpose documents",
        "ua": "Додай файли: паспорт, фото, оплати, документи мети",
    },
    {
        "id": "podpis",
        "pl": "Wyślij załącznik do e-podpisu pracodawcy / uczelni (email)",
        "ru": "Отправь приложение на e-подпись работодателю / вузу (email)",
        "en": "Send the attachment for employer / university e-signature (email)",
        "ua": "Надішли додаток на e-підпис роботодавцю / вишу (email)",
    },
    {
        "id": "upo",
        "pl": "Wyślij wniosek i pobierz UPO (potwierdzenie złożenia)",
        "ru": "Отправь заявление и скачай UPO (подтверждение подачи)",
        "en": "Submit the application and download UPO (filing confirmation)",
        "ua": "Надішли заяву і завантаж UPO (підтвердження подання)",
    },
]


def ready_finale(purpose: str | None = None, lang: str = "pl") -> dict:
    """Single screen after checklist: attachments + Open MOS + 5 portal steps."""
    lang = lang if lang in {"pl", "ru", "en", "ua"} else "pl"
    purpose_id = purpose if purpose in {p["id"] for p in PURPOSES} else "work"
    purpose_obj = next(p for p in PURPOSES if p["id"] == purpose_id)
    items_key = f"items_{lang}"
    copy = {
        "pl": {
            "title": "Wszystko gotowe — czas na MOS",
            "sub": "Poniżej: co dołączyć pod Twój cel, potem 5 kroków w oficjalnym portalu.",
            "attach_title": "Co dołączyć pod Twój cel",
            "steps_title": "Co zrobić w MOS — 5 kroków",
            "cta": "Otwórz MOS",
            "change_purpose": "Zmień cel",
        },
        "ru": {
            "title": "Всё готово — пора в MOS",
            "sub": "Ниже: что приложить под твою цель, затем 5 шагов в официальном портале.",
            "attach_title": "Что приложить под твою цель",
            "steps_title": "Что сделать в MOS — 5 шагов",
            "cta": "Открыть MOS",
            "change_purpose": "Сменить цель",
        },
        "en": {
            "title": "All set — time for MOS",
            "sub": "Below: what to attach for your purpose, then 5 steps in the official portal.",
            "attach_title": "What to attach for your purpose",
            "steps_title": "What to do in MOS — 5 steps",
            "cta": "Open MOS",
            "change_purpose": "Change purpose",
        },
        "ua": {
            "title": "Усе готово — час на MOS",
            "sub": "Нижче: що додати під твою мету, потім 5 кроків в офіційному порталі.",
            "attach_title": "Що додати під твою мету",
            "steps_title": "Що зробити в MOS — 5 кроків",
            "cta": "Відкрити MOS",
            "change_purpose": "Змінити мету",
        },
    }[lang]
    return {
        "purpose": purpose_id,
        "purpose_title": purpose_obj.get(lang, purpose_obj["pl"]),
        "attachments": purpose_obj.get(items_key, purpose_obj["items_pl"]),
        "portal_url": MOS_PORTAL_URL,
        "steps": [
            {"id": s["id"], "title": s.get(lang, s["pl"]), "n": i + 1}
            for i, s in enumerate(MOS_FILING_STEPS)
        ],
        "copy": copy,
    }


def _left_sentence(remaining: int, lang: str) -> str:
    if remaining <= 0:
        return {
            "pl": "Gotowe do oficjalnego MOS.",
            "ru": "Готово к официальному MOS.",
            "en": "Ready for official MOS.",
            "ua": "Готово до офіційного MOS.",
        }[lang]
    return {
        "pl": f"Zostało {remaining} z {len(READY_STEPS)} punktów — dziś zrób tylko ten jeden.",
        "ru": f"Осталось {remaining} из {len(READY_STEPS)} пунктов — сегодня сделай только этот.",
        "en": f"{remaining} of {len(READY_STEPS)} left — do only this one today.",
        "ua": f"Залишилось {remaining} з {len(READY_STEPS)} пунктів — сьогодні зроби лише цей.",
    }[lang]


def next_action(done: dict[str, bool] | None, lang: str = "pl") -> dict:
    """Return the first incomplete readiness step as the next action."""
    lang = lang if lang in {"pl", "ru", "en", "ua"} else "pl"
    state = done or {}
    done_count = sum(1 for s in READY_STEPS if state.get(s["id"]))
    total = len(READY_STEPS)
    for step in READY_STEPS:
        if not state.get(step["id"]):
            remaining = total - done_count
            return {
                "id": step["id"],
                "title": step.get(f"action_{lang}", step.get(lang, step["pl"])),
                "checklist_title": step.get(lang, step["pl"]),
                "hint": step.get(f"hint_{lang}", step["hint_pl"]),
                "time": step.get(f"time_{lang}", step.get("time_pl", "")),
                "link": step.get("link") or "#mos",
                "doc_id": step.get("doc_id"),
                "done_count": done_count,
                "total": total,
                "pct": int(round(100 * done_count / total)) if total else 0,
                "left": _left_sentence(remaining, lang),
                "complete": False,
            }
    return {
        "id": "open_mos",
        "title": {
            "pl": "Otwórz oficjalny MOS i złóż wniosek",
            "ru": "Открой официальный MOS и подай заявление",
            "en": "Open official MOS and file",
            "ua": "Відкрий офіційний MOS і подай заяву",
        }[lang],
        "checklist_title": {
            "pl": "Wszystko gotowe",
            "ru": "Всё готово",
            "en": "All set",
            "ua": "Усе готово",
        }[lang],
        "hint": {
            "pl": "Załóż nowe konto, zaloguj login.gov.pl, dołącz pliki, e-podpis pracodawcy, pobierz UPO.",
            "ru": "Создай новый аккаунт, войди login.gov.pl, приложи файлы, e-подпись работодателя, скачай UPO.",
            "en": "Create a new account, log in via login.gov.pl, attach files, employer e-sign, download UPO.",
            "ua": "Створи новий акаунт, увійди login.gov.pl, додай файли, e-підпис роботодавця, завантаж UPO.",
        }[lang],
        "time": {
            "pl": "oficjalny portal gov.pl",
            "ru": "официальный портал gov.pl",
            "en": "official gov.pl portal",
            "ua": "офіційний портал gov.pl",
        }[lang],
        "link": MOS_PORTAL_URL,
        "doc_id": None,
        "done_count": total,
        "total": total,
        "pct": 100,
        "left": _left_sentence(0, lang),
        "complete": True,
    }


def guide_payload(
    lang: str = "pl",
    done: dict[str, bool] | None = None,
    purpose: str | None = None,
) -> dict:
    lang = (lang or "pl").lower()
    if lang not in {"pl", "ru", "en", "ua"}:
        lang = "pl"

    ready = []
    for step in READY_STEPS:
        ready.append(
            {
                "id": step["id"],
                "title": step.get(lang, step["pl"]),
                "action": step.get(f"action_{lang}", step.get(lang, step["pl"])),
                "hint": step.get(f"hint_{lang}", step["hint_pl"]),
                "time": step.get(f"time_{lang}", step.get("time_pl", "")),
                "link": step.get("link"),
                "doc_id": step.get("doc_id"),
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
            "finale_show_checklist": "Pokaż checklistę",
            "finale_hide_checklist": "Ukryj checklistę",
            "today_label": "Dziś zrób to",
            "ready_pct_label": "Gotowość do MOS",
            "cta_do": "Zrób ten krok",
            "cta_mos": "Oficjalny MOS",
            "attach_near": "Na później — typowe załączniki",
            "more_details": "Więcej: checklista i terminy",
            "do_title": "Co robimy",
            "dont_title": "Czego nie robimy",
            "do_items": [
                "Prowadzimy Cię krok po kroku do MOS",
                "Pomagamy z checklistą, PDF i terminami",
                "Pokazujemy oficjalne linki gov.pl",
            ],
            "dont_items": [
                "Nie jesteśmy urzędem",
                "Nie składamy wniosku za Ciebie",
                "Nie zastępujemy decyzji UdSC / MOS",
            ],
            "back_to_step": "← Wróć do następnego kroku",
            "load_error": "Nie udało się wczytać przewodnika. Sprawdź sieć.",
            "retry": "Spróbuj ponownie",
            "loading": "Ładowanie następnego kroku…",
        },
        "ru": {
            "title": "Подготовка к MOS 2.0",
            "sub": "Один следующий шаг за раз. Потом официальное заявление на mos.cudzoziemcy.gov.pl.",
            "cta": "Открыть MOS",
            "info": "Справка UdSC",
            "ready_title": "Чеклист готовности",
            "purpose_title": "Выбери цель пребывания — покажем типичные приложения.",
            "walk_title": "Путь проводника",
            "next_title": "Твой следующий шаг",
            "next_done": "Всё готово",
            "do_step": "Сделать этот шаг",
            "mark_done": "Готово — дальше",
            "open_mos_btn": "Открыть MOS и подать",
            "tab_purpose": "Приложения",
            "tab_employer": "Работодателю",
            "tab_deadline": "Срок пребывания",
            "deadline_title": "Конец легального пребывания",
            "deadline_btn": "Добавить напоминание",
            "deadline_hint": "Укажи дату — сохраним срок и напомним ~за 14 дней (после входа).",
            "deadline_calendar": "Календарь аккаунта",
            "deadline_ok": "Срок и напоминание сохранены. Пункт «легальное пребывание» отмечен.",
            "deadline_login": "Войди (справа сверху), чтобы сохранить напоминание.",
            "copy_employer": "Скопировать текст",
            "copied": "Скопировано",
            "sync_account": "Прогресс сохранён в аккаунте.",
            "sync_local": "Прогресс на этом устройстве. Войди, чтобы перенести на другое.",
            "disclaimer": "WniosekPL — не ужонд и не подаёт заявление за тебя. С 27.04.2026 пребывание — в основном только online в MOS.",
            "open_mos": "Перейти на mos.cudzoziemcy.gov.pl",
            "finale_show_checklist": "Показать чеклист",
            "finale_hide_checklist": "Скрыть чеклист",
            "today_label": "Сделай сегодня",
            "ready_pct_label": "Готовность к MOS",
            "cta_do": "Сделать этот шаг",
            "cta_mos": "Официальный MOS",
            "attach_near": "На потом — типичные приложения",
            "more_details": "Ещё: чеклист и сроки",
            "do_title": "Что мы делаем",
            "dont_title": "Чего не делаем",
            "do_items": [
                "Ведём тебя шаг за шагом к MOS",
                "Помогаем с чеклистом, PDF и сроками",
                "Показываем официальные ссылки gov.pl",
            ],
            "dont_items": [
                "Мы не ужонд (не гос. орган)",
                "Не подаём заявление за тебя",
                "Не заменяем решения UdSC / MOS",
            ],
            "back_to_step": "← Вернуться к следующему шагу",
            "load_error": "Не удалось загрузить гид. Проверь интернет.",
            "retry": "Попробовать снова",
            "loading": "Загрузка следующего шага…",
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
            "finale_show_checklist": "Show checklist",
            "finale_hide_checklist": "Hide checklist",
            "today_label": "Do this today",
            "ready_pct_label": "MOS readiness",
            "cta_do": "Do this step",
            "cta_mos": "Official MOS",
            "attach_near": "For later — typical attachments",
            "more_details": "More: checklist and deadlines",
            "do_title": "What we do",
            "dont_title": "What we don’t",
            "do_items": [
                "Guide you step by step to MOS",
                "Help with checklist, PDFs and deadlines",
                "Show official gov.pl links",
            ],
            "dont_items": [
                "We are not a government office",
                "We do not file for you",
                "We do not replace UdSC / MOS decisions",
            ],
            "back_to_step": "← Back to your next step",
            "load_error": "Could not load the guide. Check your connection.",
            "retry": "Try again",
            "loading": "Loading your next step…",
        },
        "ua": {
            "title": "Підготовка до MOS 2.0",
            "sub": "Один наступний крок за раз. Потім офіційна заява на mos.cudzoziemcy.gov.pl.",
            "cta": "Відкрити MOS",
            "info": "Довідка UdSC",
            "ready_title": "Чекліст готовності",
            "purpose_title": "Обери мету перебування — покажемо типові додатки.",
            "walk_title": "Шлях провідника",
            "next_title": "Твій наступний крок",
            "next_done": "Усе готово",
            "do_step": "Зробити цей крок",
            "mark_done": "Є — далі",
            "open_mos_btn": "Відкрити MOS і подати",
            "tab_purpose": "Додатки",
            "tab_employer": "Роботодавцю",
            "tab_deadline": "Термін перебування",
            "deadline_title": "Кінець легального перебування",
            "deadline_btn": "Додати нагадування",
            "deadline_hint": "Вкажи дату — збережемо строк і нагадаємо ~за 14 днів (після входу).",
            "deadline_calendar": "Календар акаунта",
            "deadline_ok": "Строк і нагадування збережено. Пункт «легальне перебування» відмічено.",
            "deadline_login": "Увійди (справа зверху), щоб зберегти нагадування.",
            "copy_employer": "Скопіювати текст",
            "copied": "Скопійовано",
            "sync_account": "Прогрес збережено в акаунті.",
            "sync_local": "Збережено на цьому пристрої. Увійди, щоб синхронізувати.",
            "disclaimer": "WniosekPL — не ужонд і не подає заяву за тебе. З 27.04.2026 перебування здебільшого тільки online в MOS.",
            "open_mos": "Перейти на mos.cudzoziemcy.gov.pl",
            "finale_show_checklist": "Показати чекліст",
            "finale_hide_checklist": "Сховати чекліст",
            "today_label": "Зроби сьогодні",
            "ready_pct_label": "Готовність до MOS",
            "cta_do": "Зробити цей крок",
            "cta_mos": "Офіційний MOS",
            "attach_near": "На потім — типові додатки",
            "more_details": "Ще: чекліст і строки",
            "do_title": "Що ми робимо",
            "dont_title": "Чого не робимо",
            "do_items": [
                "Ведемо тебе крок за кроком до MOS",
                "Допомагаємо з чеклістом, PDF і строками",
                "Показуємо офіційні лінки gov.pl",
            ],
            "dont_items": [
                "Ми не ужонд (не держорган)",
                "Не подаємо заяву за тебе",
                "Не замінюємо рішення UdSC / MOS",
            ],
            "back_to_step": "← Повернутися до наступного кроку",
            "load_error": "Не вдалося завантажити гід. Перевір інтернет.",
            "retry": "Спробувати знову",
            "loading": "Завантаження наступного кроку…",
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

    nxt = next_action(done, lang)
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
        "next_action": nxt,
        "finale": ready_finale(purpose, lang),
    }
