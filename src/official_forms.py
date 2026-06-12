import json
from pathlib import Path

import fitz
from pypdf import PdfReader, PdfWriter

from src.address_parser import parse_polish_address, split_date, split_postal
from src.config import ROOT

OFFICIAL_DIR = ROOT / "templates" / "official"
MANIFEST_PATH = OFFICIAL_DIR / "manifest.json"

FONT = "helv"
FONT_SIZE = 9

_LATIN_MAP = str.maketrans(
    "ąćęłńóśźżĄĆĘŁŃÓŚŹŻ",
    "acelnoszzACELNOSZZ",
)


def _manifest() -> dict:
    with MANIFEST_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def template_path(doc_id: str) -> Path | None:
    entry = _manifest().get(doc_id)
    if not entry:
        return None
    path = OFFICIAL_DIR / entry["file"]
    return path if path.exists() else None


def has_official_template(doc_id: str) -> bool:
    return template_path(doc_id) is not None


def _upper(value: str) -> str:
    """WIELKIE LITERY + ASCII (urzędowe PDF często bez polskich znaków w fontach)."""
    return (value or "").strip().translate(_LATIN_MAP).upper()


def fill_pesel_official(answers: dict[str, str], output_path: Path) -> Path:
    src = template_path("pesel")
    if not src:
        raise FileNotFoundError("Official PESEL template missing")

    addr = parse_polish_address(answers.get("adres_zamieszkania", ""))
    day, month, year = split_date(answers.get("data_urodzenia", ""))
    wj_day, wj_month, wj_year = split_date(answers.get("data_wjazdu", ""))
    kod1, kod2 = split_postal(addr.kod_pocztowy)
    miejsce = answers.get("miejsce_urodzenia", "")
    kraj_urodzenia = miejsce.split(",")[-1].strip() if "," in miejsce else miejsce

    imie = _upper(answers.get("imie", ""))
    nazwisko = _upper(answers.get("nazwisko", ""))

    values = {
        "topmostSubform[0].Page1[0].Nazwisko[0]": nazwisko,
        "topmostSubform[0].Page1[0].ImięPierwsze[0]": imie,
        "topmostSubform[0].Page1[0].NazwiskoWnioskodawcy[0]": nazwisko,
        "topmostSubform[0].Page1[0].ImięWnioskodawcy[0]": imie,
        "topmostSubform[0].Page1[0].DataUrodzeniaDzień[0]": day,
        "topmostSubform[0].Page1[0].DataUrodzeniaMiesiąc[0]": month,
        "topmostSubform[0].Page1[0].DataUrodzeniaRok[0]": year,
        "topmostSubform[0].Page1[0].Ulica[0]": _upper(addr.ulica),
        "topmostSubform[0].Page1[0].NumerDomu[0]": addr.numer_domu,
        "topmostSubform[0].Page1[0].NumerLokalu[0]": addr.numer_lokalu,
        "topmostSubform[0].Page1[0].KodPocztowyCzęśćPierwsza[0]": kod1,
        "topmostSubform[0].Page1[0].KodPocztowyCzęśćDruga[0]": kod2,
        "topmostSubform[0].Page1[0].Miejscowość[0]": _upper(addr.miejscowosc),
        "topmostSubform[0].Page1[0].KrajUrodzenia[0]": _upper(kraj_urodzenia)[:40],
        "topmostSubform[0].Page1[0].KrajMiejscaZamieszkania[0]": "POLSKA",
        "topmostSubform[0].Page2[0].ImięOjcaPierwsze[0]": _upper(answers.get("imie_ojca", "")),
        "topmostSubform[0].Page2[0].ImięMatkiPierwsze[0]": _upper(answers.get("imie_matki", "")),
        "topmostSubform[0].Page2[0].MiejsceUrodzeniaNazwaMiejscowości[0]": _upper(miejsce)[:60],
        "topmostSubform[0].Page2[0].Obywatelstwo[0]": _upper(answers.get("obywatelstwo", "")),
        "topmostSubform[0].Page2[0].SeriaNumerPaszportu[0]": answers.get("numer_paszportu", "").strip(),
        "topmostSubform[0].Page3[0].DataZdarzeniaDzień[0]": wj_day,
        "topmostSubform[0].Page3[0].DataZdarzeniaMiesiąc[0]": wj_month,
        "topmostSubform[0].Page3[0].DataZdarzeniaRok[0]": wj_year,
        "topmostSubform[0].Page4[0].PodstawaPrawna[0]": (answers.get("podstawa_prawna", "").strip().translate(_LATIN_MAP))[:200],
    }

    reader = PdfReader(str(src))
    writer = PdfWriter()
    writer.append(reader)
    for page in writer.pages:
        writer.update_page_form_field_values(page, values, auto_regenerate=True)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as f:
        writer.write(f)
    return output_path


def fill_meldunek_official(
    answers: dict[str, str],
    output_path: Path,
    doc_id: str = "meldunek",
) -> Path:
    src = template_path(doc_id)
    if not src:
        raise FileNotFoundError(f"Official template missing: {doc_id}")

    addr = parse_polish_address(answers.get("adres_zamieszkania", ""))
    day, month, year = split_date(answers.get("data_urodzenia", ""))
    date_from = answers.get("data_zameldowania", "")
    birth = f"{day}-{month}-{year}" if day else ""

    overlays: list[tuple[int, float, float, str]] = [
        # Strona 1 — dane osoby
        (0, 250, 248, _upper(answers.get("nazwisko", ""))),
        (0, 250, 278, _upper(answers.get("imie", ""))),
        (0, 250, 308, answers.get("pesel", "").strip()),
        (0, 250, 348, _upper(answers.get("obywatelstwo", ""))),
        (0, 320, 388, birth),
        (0, 250, 428, _upper(answers.get("miejsce_urodzenia", ""))[:50]),
        (0, 250, 468, answers.get("numer_paszportu", "").strip()[:40]),
        # Strona 2 — adres zameldowania (EL/ZC/1 sekcja 2)
        (1, 250, 188, _upper(addr.ulica)),
        (1, 250, 218, addr.numer_domu),
        (1, 400, 218, addr.numer_lokalu),
        (1, 250, 248, addr.kod_pocztowy),
        (1, 250, 278, _upper(addr.miejscowosc)),
        (1, 320, 58, date_from[:30]),
        # Strona 3 — właściciel (do podpisu)
        (2, 250, 125, _upper(answers.get("wlasciciel_nieruchomosci", ""))[:80]),
    ]

    doc = fitz.open(str(src))
    for page_i, x, y, text in overlays:
        if not text or page_i >= len(doc):
            continue
        page = doc[page_i]
        page.insert_text(
            (x, y),
            text,
            fontname=FONT,
            fontsize=FONT_SIZE,
            color=(0, 0, 0.85),
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(output_path))
    doc.close()
    return output_path


def generate_official_pdf(doc_id: str, answers: dict[str, str], output_path: Path) -> Path:
    if doc_id == "pesel":
        return fill_pesel_official(answers, output_path)
    if doc_id in ("meldunek", "meldunek_staly"):
        return fill_meldunek_official(answers, output_path, doc_id)
    raise ValueError(f"No official template for {doc_id}")
