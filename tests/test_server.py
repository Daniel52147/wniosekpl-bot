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
    assert health.json()["documents_count"] >= 7
    assert docs.status_code == 200
    ids = {doc["id"] for doc in docs.json()}
    assert "pesel" in ids
    assert "pismo_do_urzedu" in ids
    assert meta.status_code == 200
    assert "telegram_configured" in meta.json()
    assert "web" in meta.json()["channels"]


def test_server_document_detail_and_generate(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "api.db")

    answers = {
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
    }

    with TestClient(server.app) as client:
        detail = client.get("/api/documents/pismo_do_urzedu", params={"lang": "ru"})
        pdf = client.post(
            "/api/documents/pismo_do_urzedu/generate",
            json={"user_id": 55, "lang": "ru", "answers": answers},
        )

    assert detail.status_code == 200
    assert detail.json()["id"] == "pismo_do_urzedu"
    assert len(detail.json()["fields"]) >= 8
    assert pdf.status_code == 200
    assert pdf.headers["content-type"].startswith("application/pdf")
    assert len(pdf.content) > 500


def test_server_assistant_ask_records_usage_and_enforces_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "api.db")
    monkeypatch.setattr(server, "AI_FREE_DAILY_LIMIT", 1)
    import src.config as config
    import src.entitlements as entitlements
    import src.llm as llm

    monkeypatch.setattr(config, "AI_FREE_DAILY_LIMIT", 1)
    monkeypatch.setattr(entitlements, "AI_FREE_DAILY_LIMIT", 1)
    # Keep topic classification deterministic (no live OmniRoute/LLM).
    monkeypatch.setattr(llm, "llm_configured", lambda: False)
    async def _no_llm(*args, **kwargs):
        return None
    monkeypatch.setattr(llm, "complete_chat", _no_llm)

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
    assert "/api/documents/" in page.text
    assert "generate" in page.text
