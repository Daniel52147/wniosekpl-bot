"""Проверка официальных бланков без Telegram."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.address_parser import parse_polish_address, split_date
from src.documents import load_all_documents
from src.official_forms import fill_meldunek_official, fill_pesel_official, has_official_template
from src.pdf_service import generate_document_pdf


def sample_answers(doc_id: str) -> dict[str, str]:
    base = {
        "imie": "OLENA",
        "nazwisko": "KOWALSKA",
        "data_urodzenia": "15.03.1990",
        "miejsce_urodzenia": "KYIV, UKRAINA",
        "obywatelstwo": "UKRAINA",
        "numer_paszportu": "FF123456",
        "adres_zamieszkania": "ul. Marszałkowska 10/5, 00-001 WARSZAWA",
        "imie_ojca": "IVAN",
        "imie_matki": "MARIA",
        "podstawa_prawna": "art. 7 ust. 2 ustawy o świadczeniach opieki zdrowotnej",
        "data_wjazdu": "01.01.2024",
        "data_zameldowania": "01.06.2025",
        "wlasciciel_nieruchomosci": "JAN KOWALSKI",
        "pesel": "brak",
    }
    if doc_id == "umowa_najmu":
        return {
            "wynajmujacy_imie_nazwisko": "JAN KOWALSKI",
            "wynajmujacy_adres": "ul. Testowa 1, Warszawa",
            "najemca_imie_nazwisko": "OLENA KOWALSKA",
            "najemca_dokument": "FF123456",
            "adres_lokalu": "ul. Marszałkowska 10/5, 00-001 Warszawa",
            "czynsz": "3500",
            "kaucja": "3500",
            "data_od": "01.06.2025",
            "data_do": "czas nieoznaczony",
            "media_opis": "najemca placi prad i gaz, woda w czynszu",
        }
    return base


def main() -> int:
    out_dir = ROOT / "data" / "generated" / "verify"
    out_dir.mkdir(parents=True, exist_ok=True)
    docs = load_all_documents()
    errors = []

    print("=== Official templates ===")
    for doc_id in ("pesel", "meldunek", "meldunek_staly"):
        ok = has_official_template(doc_id)
        print(f"  {doc_id}: {'OK' if ok else 'MISSING'}")

    print("\n=== Address parser ===")
    addr = parse_polish_address("ul. Marszałkowska 10/5, 00-001 WARSZAWA")
    assert addr.kod_pocztowy == "00-001", addr
    assert addr.numer_domu == "10", addr
    print(f"  ulica={addr.ulica} nr={addr.numer_domu}/{addr.numer_lokalu} kod={addr.kod_pocztowy} miasto={addr.miejscowosc}")

    print("\n=== PDF generation ===")
    fill_pesel_official(sample_answers("pesel"), out_dir / "pesel_official.pdf")
    fill_meldunek_official(sample_answers("meldunek"), out_dir / "meldunek_official.pdf", "meldunek")
    fill_meldunek_official(sample_answers("meldunek"), out_dir / "meldunek_staly_official.pdf", "meldunek_staly")
    print("  pesel_official.pdf OK")
    print("  meldunek_official.pdf OK")
    print("  meldunek_staly_official.pdf OK")

    for doc_id in docs:
        path, pdf_mode = generate_document_pdf(
            docs[doc_id],
            sample_answers(doc_id),
            out_dir / f"{doc_id}_preview.pdf",
        )
        if not path.exists() or path.stat().st_size < 1000:
            errors.append(f"{doc_id}: file too small")
        print(f"  {doc_id}: {pdf_mode} ({path.stat().st_size} B)")

    d, m, y = split_date("15.03.1990")
    if (d, m, y) != ("15", "03", "1990"):
        errors.append("split_date")

    if errors:
        print("\nERRORS:", errors)
        return 1
    print(f"\nAll OK. Output: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
