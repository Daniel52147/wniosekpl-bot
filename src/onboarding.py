"""Short onboarding → personal MOS plan."""

from __future__ import annotations

PURPOSES = ("work", "study", "family", "business")

_COPY = {
    "pl": {
        "title": "3 pytania — Twój plan",
        "sub": "Od razu wiemy, od czego zacząć. Potem jeden krok naraz.",
        "q1": "Jaki jest cel pobytu?",
        "q2": "Masz już numer PESEL?",
        "q3": "Do kiedy masz legalny pobyt?",
        "q3_hint": "Jeśli nie wiesz — pomiń. Możesz dodać datę później.",
        "yes": "Tak",
        "no": "Nie / nie wiem",
        "skip": "Nie wiem — pomiń",
        "next": "Dalej",
        "start": "Zaczynam",
        "restart": "Zmień odpowiedzi",
        "purpose": {
            "work": "Praca",
            "study": "Studia",
            "family": "Rodzina",
            "business": "Biznes",
        },
        "summary_pesel_yes": "Masz PESEL — następny krok to Profil Zaufany / login.gov.pl.",
        "summary_pesel_no": "Najpierw PESEL (albo meldunek). Potem Profil Zaufany i MOS.",
        "summary_due": "Przypomnimy przed końcem legalnego pobytu ({due}).",
        "summary_purpose": "Cel: {purpose}. Pokażemy typowe załączniki.",
    },
    "ru": {
        "title": "3 вопроса — твой план",
        "sub": "Сразу понятно, с чего начать. Потом один шаг за раз.",
        "q1": "Какая цель pobytu?",
        "q2": "У тебя уже есть PESEL?",
        "q3": "До какой даты легальный pobyt?",
        "q3_hint": "Если не знаешь — пропусти. Дату можно добавить позже.",
        "yes": "Да",
        "no": "Нет / не знаю",
        "skip": "Не знаю — пропустить",
        "next": "Дальше",
        "start": "Начать",
        "restart": "Изменить ответы",
        "purpose": {
            "work": "Работа",
            "study": "Учёба",
            "family": "Семья",
            "business": "Бизнес",
        },
        "summary_pesel_yes": "PESEL есть — следующий шаг Profil Zaufany / login.gov.pl.",
        "summary_pesel_no": "Сначала PESEL (или meldunek). Потом Profil Zaufany и MOS.",
        "summary_due": "Напомним до конца легального pobytu ({due}).",
        "summary_purpose": "Цель: {purpose}. Покажем типичные приложения.",
    },
    "en": {
        "title": "3 questions — your plan",
        "sub": "We know where to start. Then one step at a time.",
        "q1": "What is your purpose of stay?",
        "q2": "Do you already have a PESEL?",
        "q3": "Until when is your legal stay valid?",
        "q3_hint": "If you do not know — skip. You can add the date later.",
        "yes": "Yes",
        "no": "No / not sure",
        "skip": "Not sure — skip",
        "next": "Next",
        "start": "Start",
        "restart": "Change answers",
        "purpose": {
            "work": "Work",
            "study": "Studies",
            "family": "Family",
            "business": "Business",
        },
        "summary_pesel_yes": "You have PESEL — next is trusted profile / login.gov.pl.",
        "summary_pesel_no": "Start with PESEL (or meldunek). Then trusted profile and MOS.",
        "summary_due": "We will remind you before legal stay ends ({due}).",
        "summary_purpose": "Purpose: {purpose}. We will show typical attachments.",
    },
    "ua": {
        "title": "3 питання — твій план",
        "sub": "Одразу ясно, з чого почати. Потім один крок за раз.",
        "q1": "Яка мета pobytu?",
        "q2": "У тебе вже є PESEL?",
        "q3": "До якої дати легальний pobyt?",
        "q3_hint": "Якщо не знаєш — пропусти. Дату можна додати пізніше.",
        "yes": "Так",
        "no": "Ні / не знаю",
        "skip": "Не знаю — пропустити",
        "next": "Далі",
        "start": "Починаю",
        "restart": "Змінити відповіді",
        "purpose": {
            "work": "Робота",
            "study": "Навчання",
            "family": "Сім'я",
            "business": "Бізнес",
        },
        "summary_pesel_yes": "PESEL є — наступний крок Profil Zaufany / login.gov.pl.",
        "summary_pesel_no": "Спочатку PESEL (або meldunek). Потім Profil Zaufany і MOS.",
        "summary_due": "Нагадаємо до кінця легального pobytu ({due}).",
        "summary_purpose": "Мета: {purpose}. Покажемо типові додатки.",
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
