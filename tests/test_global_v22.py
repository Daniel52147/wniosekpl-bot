from fastapi.testclient import TestClient

import server
import src.database as database
from src.ai_assistant import answer_question
from src.documents import load_all_documents
from src.knowledge import _load_articles, search_knowledge
from src.ocr import ocr_engine_status
from src.packages import PACKAGES
from src.services_directory import search_services


def test_version_is_2_2():
    assert server.PRODUCT_VERSION.startswith("2.2")


def test_new_documents_loaded():
    docs = load_all_documents()
    assert "odwolanie" in docs
    assert "zaswiadczenie_zameldowania" in docs
    assert len(docs) >= 10


def test_knowledge_loads_extra_faq():
    _load_articles.cache_clear()
    hits = search_knowledge("kolejka urząd wojewódzki", "pl")
    assert any(h["id"] == "kolejka_uw" for h in hits)


def test_ai_topics_praca_and_odwolanie():
    assert answer_question("нужна работа и umowa", "ru").topic == "praca"
    assert answer_question("chcę złożyć odwołanie od odmowy", "pl").topic == "odwolanie"


def test_services_include_wroclaw():
    items = search_services(city="Wrocław")
    assert any("Wrocław" in i["city"] for i in items)


def test_packages_and_gdpr_and_calendar_api(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "v22.db")
    assert "przeprowadzka" in PACKAGES

    with TestClient(server.app) as client:
        meta = client.get("/api/meta")
        assert meta.status_code == 200
        assert meta.json()["version"].startswith("2.2")

        pkgs = client.get("/api/packages", params={"lang": "ru"})
        assert pkgs.status_code == 200
        assert pkgs.json()[0]["id"] == "przeprowadzka"

        reg = client.post(
            "/api/auth/register",
            json={
                "email": "v22@example.com",
                "password": "secret123",
                "name": "V22",
            },
        )
        token = reg.json()["session"]["token"]
        uid = reg.json()["user"]["user_id"]
        headers = {"Authorization": f"Bearer {token}"}

        client.post(
            "/api/calendar",
            headers=headers,
            json={
                "user_id": uid,
                "title": "Test termin",
                "due_at": "2026-08-01",
                "kind": "custom",
            },
        )
        cal = client.get(f"/api/calendar/{uid}", headers=headers)
        assert cal.status_code == 200
        assert len(cal.json()["items"]) >= 1
        event_id = cal.json()["items"][0]["id"]
        deleted = client.delete(
            f"/api/calendar/{event_id}",
            params={"user_id": uid},
            headers=headers,
        )
        assert deleted.status_code == 200

        export = client.get("/api/account/export", headers=headers)
        assert export.status_code == 200
        assert export.json()["user"]["email"] == "v22@example.com"

        logout = client.post("/api/auth/logout", headers=headers)
        assert logout.status_code == 200
        me = client.get("/api/auth/me", headers=headers)
        assert me.status_code == 401

        assert client.get("/robots.txt").status_code == 200
        assert client.get("/manifest.webmanifest").status_code == 200


def test_odwolanie_pdf_generates(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "pdf.db")
    with TestClient(server.app) as client:
        res = client.post(
            "/api/documents/odwolanie/generate",
            json={
                "user_id": 55,
                "lang": "pl",
                "answers": {
                    "nadawca_imie_nazwisko": "Anna Test",
                    "nadawca_adres": "Warszawa",
                    "nadawca_telefon": "500600700",
                    "organ_nazwa": "UW",
                    "organ_adres": "Warszawa",
                    "znak_sprawy": "ABC/1/2026",
                    "data_decyzji": "01.07.2026",
                    "data_otrzymania": "03.07.2026",
                    "zarzuty": "Decyzja jest niezasadna",
                    "zadanie": "Uchylenie decyzji",
                },
            },
        )
        assert res.status_code == 200
        assert res.headers["content-type"].startswith("application/pdf")


def test_ocr_ready_after_tesseract_install():
    status = ocr_engine_status()
    assert status["tesseract_binary"] is True
    assert status["ready"] is True
