from fastapi.testclient import TestClient

import server
import src.database as database


def test_server_health_and_documents(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "api.db")

    with TestClient(server.app) as client:
        health = client.get("/health")
        docs = client.get("/api/documents", params={"lang": "en"})
        meta = client.get("/api/meta")

    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert health.json()["version"] == server.PRODUCT_VERSION
    assert docs.status_code == 200
    assert any(doc["id"] == "pesel" for doc in docs.json())
    assert meta.status_code == 200
    assert meta.json()["ai_free_daily_limit"] == server.AI_FREE_DAILY_LIMIT
    assert "web" in meta.json()["channels"]


def test_server_assistant_ask_records_usage_and_enforces_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "api.db")
    monkeypatch.setattr(server, "AI_FREE_DAILY_LIMIT", 1)

    payload = {
        "user_id": 42,
        "lang": "ru",
        "question": "Я гражданин Украины и хочу карту побыту",
    }

    with TestClient(server.app) as client:
        first = client.post("/api/assistant/ask", json=payload)
        second = client.post("/api/assistant/ask", json=payload)
        meta = client.get("/api/meta", params={"user_id": 42})

    assert first.status_code == 200
    assert first.json()["topic"] == "karta_pobytu"
    assert first.json()["free_questions_left"] == 0
    assert second.status_code == 429
    assert second.json()["detail"]["upgrade_product"] == "ai_subscription"
    assert meta.json()["used_today"] == 1
    assert meta.json()["free_questions_left"] == 0


def test_server_leads_are_idempotent(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "api.db")

    payload = {"user_id": 77, "product": "ai_subscription"}

    with TestClient(server.app) as client:
        first = client.post("/api/leads", json=payload)
        second = client.post("/api/leads", json=payload)

    assert first.status_code == 200
    assert first.json() == {"product": "ai_subscription", "created": True}
    assert second.status_code == 200
    assert second.json() == {"product": "ai_subscription", "created": False}


def test_landing_page_serves_product_ui(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "api.db")

    with TestClient(server.app) as client:
        page = client.get("/")

    assert page.status_code == 200
    assert "AI-asystent" in page.text
    assert "/api/assistant/ask" in page.text
