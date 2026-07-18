"""New-user journey copy: simple management + official MOS path."""

from __future__ import annotations

from src.mos_guide import MOS_INFO_URL, MOS_PORTAL_URL

OFFICIAL_LINKS = [
    {
        "id": "mos",
        "url": MOS_PORTAL_URL,
        "pl": "MOS 2.0 (gov)",
        "ru": "MOS 2.0 (gov)",
        "en": "MOS 2.0 (gov)",
        "ua": "MOS 2.0 (gov)",
    },
    {
        "id": "udsc",
        "url": "https://www.gov.pl/web/udsc",
        "pl": "UdSC · gov.pl",
        "ru": "UdSC · gov.pl",
        "en": "UdSC · gov.pl",
        "ua": "UdSC · gov.pl",
    },
    {
        "id": "pz",
        "url": "https://www.gov.pl/web/gov/zaloz-profil-zaufany",
        "pl": "Profil Zaufany",
        "ru": "Profil Zaufany",
        "en": "Trusted profile",
        "ua": "Profil Zaufany",
    },
    {
        "id": "info",
        "url": MOS_INFO_URL,
        "pl": "Info MOS",
        "ru": "Info MOS",
        "en": "MOS info",
        "ua": "Info MOS",
    },
]

_COPY = {
    "pl": {
        "official_kicker": "Oficjalna ścieżka",
        "official_note": "WniosekPL pomaga przygotować się. Wniosek składasz tylko na mos.cudzoziemcy.gov.pl — to portal UdSC.",
        "path_title": "Jak to działa — 3 etapy",
        "path": [
            {
                "id": "prepare",
                "title": "1. Przygotuj",
                "body": "PESEL, Profil Zaufany, skany, załączniki. My prowadzimy checklistę.",
            },
            {
                "id": "check",
                "title": "2. Sprawdź",
                "body": "Gdy wszystko gotowe — zobaczysz listę plików i 5 kroków w MOS.",
            },
            {
                "id": "file",
                "title": "3. Złóż w MOS",
                "body": "Otwórz oficjalny portal, wyślij wniosek i pobierz UPO.",
            },
        ],
        "how_title": "Jak korzystać z profilu",
        "how_items": [
            "Zakładka Teraz — tylko Twój następny krok.",
            "Dokumenty — wypełnij PDF (pola zapisują się same).",
            "Konto — logowanie, Telegram i płatności.",
        ],
        "how_dismiss": "Rozumiem",
        "cabinet_title": "Twój profil",
        "cabinet_sub": "Jeden następny krok do oficjalnego MOS. Reszta — w zakładkach poniżej.",
        "tab_now": "Teraz",
        "tab_now_hint": "Następny krok",
        "tab_docs": "Dokumenty",
        "tab_docs_hint": "PDF",
        "tab_account": "Konto",
        "tab_account_hint": "Login / Telegram",
        "crumb": " · Przygotowanie do oficjalnego MOS",
        "landing_cta": "Zacznij przygotowanie",
        "landing_path_title": "Oficjalna droga do wniosku",
        "landing_path_sub": "Najpierw przygotowanie u nas — złożenie tylko w MOS na gov.pl.",
    },
    "ru": {
        "official_kicker": "Официальный путь",
        "official_note": "WniosekPL помогает подготовиться. Wniosek подаёшь только на mos.cudzoziemcy.gov.pl — портал UdSC.",
        "path_title": "Как это работает — 3 этапа",
        "path": [
            {
                "id": "prepare",
                "title": "1. Подготовь",
                "body": "PESEL, Profil Zaufany, сканы, приложения. Мы ведём чеклист.",
            },
            {
                "id": "check",
                "title": "2. Проверь",
                "body": "Когда всё готово — список файлов и 5 шагов в MOS.",
            },
            {
                "id": "file",
                "title": "3. Подай в MOS",
                "body": "Открой официальный портал, отправь wniosek и скачай UPO.",
            },
        ],
        "how_title": "Как пользоваться профилем",
        "how_items": [
            "Вкладка Teraz — только твой следующий шаг.",
            "Dokumenty — заполни PDF (поля сохраняются сами).",
            "Konto — вход, Telegram и оплата.",
        ],
        "how_dismiss": "Понятно",
        "cabinet_title": "Твой профиль",
        "cabinet_sub": "Один следующий шаг к официальному MOS. Остальное — во вкладках ниже.",
        "tab_now": "Сейчас",
        "tab_now_hint": "Следующий шаг",
        "tab_docs": "Документы",
        "tab_docs_hint": "PDF",
        "tab_account": "Аккаунт",
        "tab_account_hint": "Вход / Telegram",
        "crumb": " · Подготовка к официальному MOS",
        "landing_cta": "Начать подготовку",
        "landing_path_title": "Официальный путь к wniosek",
        "landing_path_sub": "Сначала подготовка у нас — подача только в MOS на gov.pl.",
    },
    "en": {
        "official_kicker": "Official path",
        "official_note": "WniosekPL helps you prepare. You file only at mos.cudzoziemcy.gov.pl — the UdSC portal.",
        "path_title": "How it works — 3 stages",
        "path": [
            {
                "id": "prepare",
                "title": "1. Prepare",
                "body": "PESEL, trusted profile, scans, attachments. We run the checklist.",
            },
            {
                "id": "check",
                "title": "2. Review",
                "body": "When ready — see the file list and 5 steps inside MOS.",
            },
            {
                "id": "file",
                "title": "3. File in MOS",
                "body": "Open the official portal, submit, download UPO.",
            },
        ],
        "how_title": "How to use your profile",
        "how_items": [
            "Now tab — only your next step.",
            "Documents — fill PDFs (fields save automatically).",
            "Account — login, Telegram and billing.",
        ],
        "how_dismiss": "Got it",
        "cabinet_title": "Your profile",
        "cabinet_sub": "One next step toward official MOS. Everything else is in the tabs below.",
        "tab_now": "Now",
        "tab_now_hint": "Next step",
        "tab_docs": "Documents",
        "tab_docs_hint": "PDFs",
        "tab_account": "Account",
        "tab_account_hint": "Login / Telegram",
        "crumb": " · Preparing for official MOS",
        "landing_cta": "Start preparing",
        "landing_path_title": "Official path to your application",
        "landing_path_sub": "Prepare here first — file only in MOS on gov.pl.",
    },
    "ua": {
        "official_kicker": "Офіційний шлях",
        "official_note": "WniosekPL допомагає підготуватися. Wniosek подаєш лише на mos.cudzoziemcy.gov.pl — портал UdSC.",
        "path_title": "Як це працює — 3 етапи",
        "path": [
            {
                "id": "prepare",
                "title": "1. Підготуй",
                "body": "PESEL, Profil Zaufany, скани, додатки. Ми ведемо чекліст.",
            },
            {
                "id": "check",
                "title": "2. Перевір",
                "body": "Коли все готово — список файлів і 5 кроків у MOS.",
            },
            {
                "id": "file",
                "title": "3. Подай у MOS",
                "body": "Відкрий офіційний портал, надішли wniosek і завантаж UPO.",
            },
        ],
        "how_title": "Як користуватися профілем",
        "how_items": [
            "Вкладка Teraz — лише твій наступний крок.",
            "Dokumenty — заповни PDF (поля зберігаються самі).",
            "Konto — вхід, Telegram і оплата.",
        ],
        "how_dismiss": "Зрозуміло",
        "cabinet_title": "Твій профіль",
        "cabinet_sub": "Один наступний крок до офіційного MOS. Інше — у вкладках нижче.",
        "tab_now": "Зараз",
        "tab_now_hint": "Наступний крок",
        "tab_docs": "Документи",
        "tab_docs_hint": "PDF",
        "tab_account": "Акаунт",
        "tab_account_hint": "Вхід / Telegram",
        "crumb": " · Підготовка до офіційного MOS",
        "landing_cta": "Почати підготовку",
        "landing_path_title": "Офіційний шлях до wniosku",
        "landing_path_sub": "Спочатку підготовка в нас — подання лише в MOS на gov.pl.",
    },
}


def guide_ux_payload(lang: str = "pl", stage: str = "prepare") -> dict:
    lang = lang if lang in _COPY else "pl"
    stage = stage if stage in {"prepare", "check", "file"} else "prepare"
    copy = _COPY[lang]
    return {
        "lang": lang,
        "stage": stage,
        "copy": {
            k: v
            for k, v in copy.items()
            if k != "path"
        },
        "path": copy["path"],
        "official_links": [
            {"id": x["id"], "url": x["url"], "label": x.get(lang, x["pl"])}
            for x in OFFICIAL_LINKS
        ],
        "portal_url": MOS_PORTAL_URL,
        "info_url": MOS_INFO_URL,
    }
