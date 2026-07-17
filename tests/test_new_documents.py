from pathlib import Path

from src.documents import load_all_documents
from src.pdf_service import generate_document_pdf


NEW_DOCS = ("pismo_do_urzedu", "upowaznienie", "oswiadczenie_dochodow")


def test_new_helper_documents_are_loaded():
    docs = load_all_documents()
    for doc_id in NEW_DOCS:
        assert doc_id in docs
        assert len(docs[doc_id].fields) >= 6


def test_generate_helper_pdfs_for_new_documents(tmp_path):
    docs = load_all_documents()
    samples = {
        "pismo_do_urzedu": {
            "nadawca_imie_nazwisko": "Olena Kowalska",
            "nadawca_adres": "ul. Testowa 1, 00-001 Warszawa",
            "nadawca_telefon": "+48123123123",
            "urzad_nazwa": "Urzad Wojewodzki",
            "urzad_adres": "ul. Urzedowa 2, Warszawa",
            "znak_sprawy": "WU/1/2026",
            "temat_pisma": "Uzupełnienie dokumentów",
            "tresc_pisma": "Przesylam brakujace dokumenty.",
            "data_pisma": "17.07.2026",
            "miejscowosc_pisma": "Warszawa",
        },
        "upowaznienie": {
            "mocodawca_imie_nazwisko": "Olena Kowalska",
            "mocodawca_dokument": "FF123456",
            "mocodawca_adres": "ul. Testowa 1, 00-001 Warszawa",
            "pelnomocnik_imie_nazwisko": "Jan Nowak",
            "pelnomocnik_dokument": "ABC123456",
            "zakres_upowaznienia": "zlozenie dokumentow do karty pobytu",
            "urzad_nazwa": "Urzad Wojewodzki",
            "data_upowaznienia": "17.07.2026",
            "miejscowosc_upowaznienia": "Warszawa",
        },
        "oswiadczenie_dochodow": {
            "imie": "Olena",
            "nazwisko": "Kowalska",
            "data_urodzenia": "15.03.1990",
            "adres_zamieszkania": "ul. Testowa 1, 00-001 Warszawa",
            "zrodlo_dochodu": "umowa o prace",
            "pracodawca_nazwa": "ACME Sp. z o.o.",
            "dochod_miesieczny": "4500",
            "okres_dochodu": "styczen-czerwiec 2026",
            "data_oswiadczenia": "17.07.2026",
            "miejscowosc_oswiadczenia": "Warszawa",
        },
    }

    for doc_id, answers in samples.items():
        path, mode = generate_document_pdf(
            docs[doc_id],
            answers,
            Path(tmp_path) / f"{doc_id}.pdf",
        )
        assert mode == "helper"
        assert path.exists()
        assert path.stat().st_size > 500
