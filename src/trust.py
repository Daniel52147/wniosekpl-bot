"""Trust / FAQ copy for landing and cabinet (not a government office)."""

from __future__ import annotations

GOV_LINKS = [
    {
        "id": "mos",
        "url": "https://mos.cudzoziemcy.gov.pl",
        "pl": "MOS 2.0 — oficjalny portal",
        "ru": "MOS 2.0 — официальный портал",
        "en": "MOS 2.0 — official portal",
        "ua": "MOS 2.0 — офіційний портал",
    },
    {
        "id": "udsc",
        "url": "https://www.gov.pl/web/udsc",
        "pl": "Urząd do Spraw Cudzoziemców (gov.pl)",
        "ru": "Управление по делам иностранцев (gov.pl)",
        "en": "Office for Foreigners (gov.pl)",
        "ua": "Управління у справах іноземців (gov.pl)",
    },
    {
        "id": "pz",
        "url": "https://www.gov.pl/web/gov/zaloz-profil-zaufany",
        "pl": "Profil Zaufany — gov.pl",
        "ru": "Profil Zaufany — gov.pl",
        "en": "Trusted profile — gov.pl",
        "ua": "Profil Zaufany — gov.pl",
    },
]

CONTACT_EMAIL = "hello@wniosekpl.pl"

FAQ = [
    {
        "id": "not_office",
        "q_pl": "Czy jesteście urzędem?",
        "a_pl": "Nie. WniosekPL to prywatny przewodnik. Oficjalny wniosek składasz tylko w MOS na mos.cudzoziemcy.gov.pl.",
        "q_ru": "Вы — urząd?",
        "a_ru": "Нет. WniosekPL — частный гид. Официальный wniosek подаёшь только в MOS на mos.cudzoziemcy.gov.pl.",
        "q_en": "Are you a government office?",
        "a_en": "No. WniosekPL is a private guide. You file only in MOS at mos.cudzoziemcy.gov.pl.",
        "q_ua": "Ви — urząd?",
        "a_ua": "Ні. WniosekPL — приватний гід. Офіційний wniosek подаєш лише в MOS на mos.cudzoziemcy.gov.pl.",
    },
    {
        "id": "legal",
        "q_pl": "Czy to porada prawna?",
        "a_pl": "Nie. Pomagamy przygotować checklistę, PDF i pytania. W sprawach złożonych skonsultuj prawnika lub urząd.",
        "q_ru": "Это юридическая консультация?",
        "a_ru": "Нет. Мы помогаем с чеклистом, PDF и вопросами. В сложных делах — юрист или urząd.",
        "q_en": "Is this legal advice?",
        "a_en": "No. We help with checklists, PDFs and questions. For complex cases, see a lawyer or the office.",
        "q_ua": "Це юридична консультація?",
        "a_ua": "Ні. Ми допомагаємо з чеклістом, PDF і питаннями. У складних справах — юрист або urząd.",
    },
    {
        "id": "data",
        "q_pl": "Co z moimi danymi?",
        "a_pl": "Postęp i szkice formularzy zapisujemy na Twoim koncie, żeby wrócić później. Nie składamy wniosku w Twoim imieniu.",
        "q_ru": "Что с моими данными?",
        "a_ru": "Прогресс и черновики форм храним в аккаунте, чтобы вернуться позже. Заявление за тебя не подаём.",
        "q_en": "What about my data?",
        "a_en": "We store progress and form drafts on your account so you can resume. We do not file on your behalf.",
        "q_ua": "Що з моїми даними?",
        "a_ua": "Прогрес і чернетки форм зберігаємо в акаунті, щоб повернутися пізніше. Заяву за тебе не подаємо.",
    },
    {
        "id": "mos_only",
        "q_pl": "Gdzie składasz wniosek o pobyt?",
        "a_pl": "Od 27.04.2026 pobyt czasowy/stały/rezydent UE — zasadniczo tylko online w MOS 2.0.",
        "q_ru": "Где подавать wniosek о pobyt?",
        "a_ru": "С 27.04.2026 pobyt — в основном только online в MOS 2.0.",
        "q_en": "Where do I file a residence application?",
        "a_en": "Since 27 Apr 2026 residence permits are mostly online-only via MOS 2.0.",
        "q_ua": "Де подавати wniosek про pobyt?",
        "a_ua": "З 27.04.2026 pobyt здебільшого тільки online в MOS 2.0.",
    },
    {
        "id": "contact",
        "q_pl": "Jak się z Wami skontaktować?",
        "a_pl": f"Napisz na {CONTACT_EMAIL} albo przez bota Telegram @wniosekpl_bot.",
        "q_ru": "Как с вами связаться?",
        "a_ru": f"Напиши на {CONTACT_EMAIL} или боту Telegram @wniosekpl_bot.",
        "q_en": "How can I contact you?",
        "a_en": f"Email {CONTACT_EMAIL} or Telegram bot @wniosekpl_bot.",
        "q_ua": "Як з вами звʼязатися?",
        "a_ua": f"Напиши на {CONTACT_EMAIL} або боту Telegram @wniosekpl_bot.",
    },
]


def trust_payload(lang: str = "pl") -> dict:
    lang = lang if lang in {"pl", "ru", "en", "ua"} else "pl"
    headlines = {
        "pl": {
            "kicker": "Zaufanie",
            "title": "Nie jesteśmy urzędem",
            "body": "Pomagamy przygotować się do MOS. Oficjalne decyzje i złożenie wniosku — tylko na gov.pl / MOS.",
            "gov_title": "Oficjalne źródła",
            "faq_title": "Krótki FAQ",
            "contact": "Kontakt",
            "contact_cta": "Napisz do nas",
        },
        "ru": {
            "kicker": "Доверие",
            "title": "Мы не urząd",
            "body": "Помогаем подготовиться к MOS. Официальные решения и подача — только на gov.pl / MOS.",
            "gov_title": "Официальные источники",
            "faq_title": "Короткий FAQ",
            "contact": "Контакт",
            "contact_cta": "Написать нам",
        },
        "en": {
            "kicker": "Trust",
            "title": "We are not a government office",
            "body": "We help you prepare for MOS. Official decisions and filing happen only on gov.pl / MOS.",
            "gov_title": "Official sources",
            "faq_title": "Short FAQ",
            "contact": "Contact",
            "contact_cta": "Email us",
        },
        "ua": {
            "kicker": "Довіра",
            "title": "Ми не urząd",
            "body": "Допомагаємо підготуватися до MOS. Офіційні рішення і подання — лише на gov.pl / MOS.",
            "gov_title": "Офіційні джерела",
            "faq_title": "Короткий FAQ",
            "contact": "Контакт",
            "contact_cta": "Написати нам",
        },
    }
    links = [
        {"id": g["id"], "url": g["url"], "label": g.get(lang, g["pl"])}
        for g in GOV_LINKS
    ]
    faq = [
        {
            "id": item["id"],
            "q": item.get(f"q_{lang}", item["q_pl"]),
            "a": item.get(f"a_{lang}", item["a_pl"]),
        }
        for item in FAQ
    ]
    return {
        "lang": lang,
        "copy": headlines[lang],
        "gov_links": links,
        "faq": faq,
        "contact_email": CONTACT_EMAIL,
    }
