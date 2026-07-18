"""Short onboarding → personal MOS plan."""

from __future__ import annotations

PURPOSES = ("work", "study", "family", "business")

_COPY = {
    "pl": {
        "title": "Start: 3 krótkie pytania",
        "sub": "Ułożymy oficjalną ścieżkę do MOS. Wniosek i tak złożysz tylko na mos.cudzoziemcy.gov.pl.",
        "q1": "Jaki jest cel pobytu?",
        "q2": "Masz już numer PESEL?",
        "q3": "Do kiedy masz legalny pobyt?",
        "q3_hint": "Jeśli nie wiesz — pomiń. Datę możesz dodać później w zakładce Teraz.",
        "yes": "Tak",
        "no": "Nie / nie wiem",
        "skip": "Nie wiem — pomiń",
        "next": "Dalej",
        "start": "Pokaż mój następny krok",
        "restart": "Zmień odpowiedzi",
        "purpose": {
            "work": "Praca",
            "study": "Studia",
            "family": "Rodzina",
            "business": "Biznes",
        },
        "summary_pesel_yes": "Masz PESEL — następny krok: Profil Zaufany / login.gov.pl (gov.pl).",
        "summary_pesel_no": "Najpierw PESEL (lub meldunek). Potem Profil Zaufany i oficjalny MOS.",
        "summary_due": "Przypomnimy przed końcem legalnego pobytu ({due}).",
        "summary_purpose": "Cel: {purpose}. Pokażemy typowe załączniki do MOS.",
    },
    "ru": {
        "title": "Старт: 3 коротких вопроса",
        "sub": "Составим официальный путь к MOS. Wniosek всё равно подаёшь только на mos.cudzoziemcy.gov.pl.",
        "q1": "Какая цель pobytu?",
        "q2": "У тебя уже есть PESEL?",
        "q3": "До какой даты легальный pobyt?",
        "q3_hint": "Если не знаешь — пропусти. Дату можно добавить позже во вкладке Teraz.",
        "yes": "Да",
        "no": "Нет / не знаю",
        "skip": "Не знаю — пропустить",
        "next": "Дальше",
        "start": "Показать мой следующий шаг",
        "restart": "Изменить ответы",
        "purpose": {
            "work": "Работа",
            "study": "Учёба",
            "family": "Семья",
            "business": "Бизнес",
        },
        "summary_pesel_yes": "PESEL есть — следующий шаг: Profil Zaufany / login.gov.pl (gov.pl).",
        "summary_pesel_no": "Сначала PESEL (или meldunek). Потом Profil Zaufany и официальный MOS.",
        "summary_due": "Напомним до конца легального pobytu ({due}).",
        "summary_purpose": "Цель: {purpose}. Покажем типичные приложения для MOS.",
    },
    "en": {
        "title": "Start: 3 short questions",
        "sub": "We build your official path to MOS. You still file only at mos.cudzoziemcy.gov.pl.",
        "q1": "What is your purpose of stay?",
        "q2": "Do you already have a PESEL?",
        "q3": "Until when is your legal stay valid?",
        "q3_hint": "If you do not know — skip. You can add the date later in the Now tab.",
        "yes": "Yes",
        "no": "No / not sure",
        "skip": "Not sure — skip",
        "next": "Next",
        "start": "Show my next step",
        "restart": "Change answers",
        "purpose": {
            "work": "Work",
            "study": "Studies",
            "family": "Family",
            "business": "Business",
        },
        "summary_pesel_yes": "You have PESEL — next: trusted profile / login.gov.pl (gov.pl).",
        "summary_pesel_no": "Start with PESEL (or meldunek). Then trusted profile and official MOS.",
        "summary_due": "We will remind you before legal stay ends ({due}).",
        "summary_purpose": "Purpose: {purpose}. We will show typical MOS attachments.",
    },
    "ua": {
        "title": "Старт: 3 короткі питання",
        "sub": "Складемо офіційний шлях до MOS. Wniosek усе одно подаєш лише на mos.cudzoziemcy.gov.pl.",
        "q1": "Яка мета pobytu?",
        "q2": "У тебе вже є PESEL?",
        "q3": "До якої дати легальний pobyt?",
        "q3_hint": "Якщо не знаєш — пропусти. Дату можна додати пізніше у вкладці Teraz.",
        "yes": "Так",
        "no": "Ні / не знаю",
        "skip": "Не знаю — пропустити",
        "next": "Далі",
        "start": "Показати мій наступний крок",
        "restart": "Змінити відповіді",
        "purpose": {
            "work": "Робота",
            "study": "Навчання",
            "family": "Сім'я",
            "business": "Бізнес",
        },
        "summary_pesel_yes": "PESEL є — наступний крок: Profil Zaufany / login.gov.pl (gov.pl).",
        "summary_pesel_no": "Спочатку PESEL (або meldunek). Потім Profil Zaufany і офіційний MOS.",
        "summary_due": "Нагадаємо до кінця легального pobytu ({due}).",
        "summary_purpose": "Мета: {purpose}. Покажемо типові додатки для MOS.",
    },
}


def copy_for(lang: str) -> dict:
    return _COPY[lang if lang in _COPY else "pl"]


def build_plan(
    purpose: str,
    has_pesel: bool,
    due_at: str | None = None,
    lang: str = "pl",
) -> dict:
    purpose = purpose if purpose in PURPOSES else "work"
    c = copy_for(lang)
    purpose_label = c["purpose"][purpose]
    lines = [
        c["summary_purpose"].format(purpose=purpose_label),
        c["summary_pesel_yes"] if has_pesel else c["summary_pesel_no"],
    ]
    if due_at:
        lines.append(c["summary_due"].format(due=due_at[:10]))
    first = "trusted_profile" if has_pesel else "pesel"
    return {
        "purpose": purpose,
        "has_pesel": has_pesel,
        "due_at": (due_at or "")[:10] or None,
        "first_step": first,
        "summary_lines": lines,
        "copy": c,
    }
