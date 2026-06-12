from src.documents import load_all_documents
from src.packages import build_answers_for_doc, fields_to_ask, package_field_sequence


def test_package_field_sequence_covers_shared_fields():
    docs = load_all_documents()
    seq = package_field_sequence(docs)
    keys = [f.key for f in seq]
    assert keys[0] == "imie"
    assert "podstawa_prawna" in keys
    assert "data_wjazdu" in keys
    assert len(seq) >= 15


def test_build_answers_umowa_aliases():
    docs = load_all_documents()
    doc = docs["umowa_najmu"]
    shared = {
        "imie": "Jan",
        "nazwisko": "Kowalski",
        "numer_paszportu": "AB123456",
        "adres_zamieszkania": "ul. Test 1, 00-001 Warszawa",
        "wlasciciel_nieruchomosci": "Anna Nowak",
    }
    answers = build_answers_for_doc(doc, shared)
    assert "Jan Kowalski" in answers.get("najemca_imie_nazwisko", "")
    assert answers.get("najemca_dokument") == "AB123456"


def test_fields_to_ask_skips_filled():
    docs = load_all_documents()
    doc = docs["pesel"]
    answers = {"imie": "Jan", "nazwisko": "Kowalski"}
    remaining = fields_to_ask(doc, answers)
    assert all(f.key not in ("imie", "nazwisko") for f in remaining)
