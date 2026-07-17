from src.llm import complete_chat


def fallback_letter(payload: dict, lang: str) -> str:
    topic = payload.get("topic") or payload.get("temat") or "Sprawa urzędowa"
    body = payload.get("content") or payload.get("tresc") or ""
    name = payload.get("name") or "Imię i nazwisko"
    city = payload.get("city") or "Warszawa"
    date = payload.get("date") or "DD.MM.RRRR"
    office = payload.get("office") or "Urząd"
    case_no = payload.get("case_no") or "brak"

    if lang == "en":
        return (
            f"{city}, {date}\n\n"
            f"To: {office}\n"
            f"Case number: {case_no}\n"
            f"Subject: {topic}\n\n"
            f"Dear Sir or Madam,\n\n{body}\n\nYours sincerely,\n{name}"
        )
    return (
        f"{city}, dnia {date}\n\n"
        f"Do: {office}\n"
        f"Znak sprawy: {case_no}\n"
        f"Dotyczy: {topic}\n\n"
        f"Szanowni Państwo,\n\n{body}\n\nZ poważaniem,\n{name}"
    )


async def write_official_letter(payload: dict, lang: str) -> dict:
    system = (
        "You help foreigners in Poland write polite official letters in Polish. "
        "Return only the letter text. Not legal advice. Keep facts from the user."
    )
    user = (
        f"User language preference: {lang}\n"
        f"Write a Polish official letter using these facts:\n{payload}"
    )
    llm_text = await complete_chat(system, user)
    text = llm_text or fallback_letter(payload, lang)
    return {"mode": "llm" if llm_text else "template", "letter": text}
