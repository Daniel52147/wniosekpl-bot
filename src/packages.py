from dataclasses import dataclass

from src.documents import DocumentDef


@dataclass
class PackageDef:
    id: str
    title_ru: str
    title_en: str
    title_ua: str
    title_pl: str
    doc_order: list[str]
    intro_ru: str
    intro_en: str
    intro_ua: str
    intro_pl: str = ""

    def title(self, lang: str) -> str:
        return {
            "ru": self.title_ru,
            "en": self.title_en,
            "ua": self.title_ua,
            "pl": self.title_pl,
        }.get(lang, self.title_ru)

    def intro(self, lang: str) -> str:
        return {
            "ru": self.intro_ru,
            "en": self.intro_en,
            "ua": self.intro_ua,
            "pl": self.intro_pl or self.intro_ru,
        }.get(lang, self.intro_ru)


PRZEPROWADZKA = PackageDef(
    id="przeprowadzka",
    title_ru="📦 Пакет «Переезд»",
    title_en="📦 Relocation package",
    title_ua="📦 Пакет «Переїзд»",
    title_pl="📦 Pakiet Przeprowadzka",
    doc_order=["umowa_najmu", "meldunek", "pesel"],
    intro_ru=(
        "Один раз ответите на общие вопросы — получите <b>3 PDF</b>:\n"
        "umowa najmu → meldunek → PESEL.\n\n"
        "Данные переносятся между документами."
    ),
    intro_en=(
        "Answer shared questions once — get <b>3 PDFs</b>:\n"
        "rental → meldunek → PESEL."
    ),
    intro_ua=(
        "Один раз відповіді — <b>3 PDF</b>:\n"
        "umowa → meldunek → PESEL."
    ),
    intro_pl=(
        "Odpowiedz na wspólne pytania — dostaniesz <b>3 PDF</b>:\n"
        "umowa najmu → meldunek → PESEL.\n\n"
        "Dane przenoszą się między dokumentami."
    ),
)

PACKAGES: dict[str, PackageDef] = {PRZEPROWADZKA.id: PRZEPROWADZKA}

# Kolejność wspólnych pytań w pakiecie «Przeprowadzka»
PACKAGE_FIELD_ORDER: list[str] = [
    "imie",
    "nazwisko",
    "data_urodzenia",
    "miejsce_urodzenia",
    "obywatelstwo",
    "numer_paszportu",
    "adres_zamieszkania",
    "wlasciciel_nieruchomosci",
    "wynajmujacy_adres",
    "czynsz",
    "kaucja",
    "data_od",
    "data_do",
    "media_opis",
    "data_zameldowania",
    "pesel",
    "podstawa_prawna",
    "imie_ojca",
    "imie_matki",
    "data_wjazdu",
]


def package_field_sequence(docs: dict[str, DocumentDef]) -> list:
    seen: set[str] = set()
    result = []
    for key in PACKAGE_FIELD_ORDER:
        if key in seen:
            continue
        for doc_id in PRZEPROWADZKA.doc_order:
            doc = docs.get(doc_id)
            if not doc:
                continue
            for field in doc.fields:
                if field.key == key:
                    result.append(field)
                    seen.add(key)
                    break
    return result


def build_answers_for_doc(
    doc: DocumentDef, shared: dict[str, str]
) -> dict[str, str]:
    """Map shared profile onto document fields + umowa aliases."""
    answers = {k: v for k, v in shared.items() if v}

    if doc.id == "umowa_najmu":
        if shared.get("imie") and shared.get("nazwisko"):
            answers.setdefault(
                "najemca_imie_nazwisko",
                f"{shared['imie']} {shared['nazwisko']}".strip(),
            )
        answers.setdefault("najemca_dokument", shared.get("numer_paszportu", ""))
        answers.setdefault("adres_lokalu", shared.get("adres_zamieszkania", ""))
        answers.setdefault(
            "wynajmujacy_imie_nazwisko",
            shared.get("wlasciciel_nieruchomosci", ""),
        )
        answers.setdefault("wynajmujacy_adres", shared.get("wynajmujacy_adres", ""))

    return answers


def fields_to_ask(doc: DocumentDef, answers: dict[str, str]) -> list:
    return [f for f in doc.fields if not (answers.get(f.key) or "").strip()]
