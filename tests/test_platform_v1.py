import asyncio
from pathlib import Path

from fastapi.testclient import TestClient

import server
import src.database as database
from src.knowledge import search_knowledge
from src.karta_wizard import default_progress, progress_view
from src.letter_writer import fallback_letter
from src.services_directory import search_services


def test_knowledge_search_finds_pesel():
    hits = search_knowledge("как получить pesel в gminie", "ru")
    assert hits
    assert hits[0]["id"] == "pesel"


def test_karta_wizard_progress_defaults():
    view = progress_view(default_progress(), "en")
    assert len(view) >= 6
    assert all("title" in step for step in view)


def test_services_directory_warsaw():
    items = search_services(city="Warszawa")
    assert any("Wojewódzki" in i["name"] for i in items)


def test_fallback_letter_contains_polish_greeting():
    text = fallback_letter(
        {
            "name": "Olena",
            "city": "Warszawa",
            "date": "17.07.2026",
            "office": "UW",
            "topic": "Dokumenty",
            "content": "Prosze o przyjecie dokumentow.",
        },
        "ru",
    )
    assert "Szanowni Państwo" in text


def test_platform_billing_cabinet_karta_and_letter(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "platform.db")

    with TestClient(server.app) as client:
        meta = client.get("/api/meta", params={"user_id": 101})
        assert meta.status_code == 200
        assert meta.json()["version"].startswith("2.")

        checkout = client.post(
            "/api/billing/checkout",
            json={"user_id": 101, "product": "ai_subscription"},
        )
        assert checkout.status_code == 200
        assert "checkout_url" in checkout.json()

        complete = client.get(
            "/api/billing/mock-complete",
            params={"user_id": 101, "product": "ai_subscription"},
            follow_redirects=False,
        )
        assert complete.status_code in (302, 307)

        cabinet = client.get("/api/cabinet/101")
        assert cabinet.status_code == 200
        assert cabinet.json()["plan"]["unlimited"] is True

        karta = client.get("/api/karta/101", params={"lang": "ru"})
        assert karta.status_code == 200
        step_id = karta.json()["steps"][0]["id"]
        updated = client.post(
            "/api/karta/step",
            json={"user_id": 101, "step_id": step_id, "done": True},
        )
        assert updated.status_code == 200
        assert updated.json()["steps"][0]["done"] is True

        letter = client.post(
            "/api/letters/generate",
            json={
                "user_id": 101,
                "lang": "pl",
                "name": "Olena Kowalska",
                "city": "Warszawa",
                "office": "Urzad Wojewodzki",
                "case_no": "A/1",
                "topic": "Uzupelnienie",
                "content": "Przesylam dokumenty.",
            },
        )
        assert letter.status_code == 200
        assert "Szanowni Państwo" in letter.json()["letter"]

        docs = client.get("/api/documents")
        ids = {d["id"] for d in docs.json()}
        assert "karta_pobytu_przygotowanie" in ids
        assert len(ids) >= 8
