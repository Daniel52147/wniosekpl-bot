from fastapi.testclient import TestClient

import server
import src.config as config
import src.database as database
from src.countries import list_countries
from src.marketplace import list_lawyers
from src.payments import parse_checkout_completed


def test_countries_include_live_poland():
    items = list_countries()
    assert any(c["code"] == "pl" and c["status"] == "live" for c in items)


def test_lawyers_marketplace_has_entries():
    assert len(list_lawyers()) >= 3


def test_parse_checkout_completed():
    event = {
        "type": "checkout.session.completed",
        "data": {
            "object": {
                "id": "cs_test_123",
                "client_reference_id": "42",
                "metadata": {"user_id": "42", "product": "ai_subscription"},
                "payment_status": "paid",
            }
        },
    }
    parsed = parse_checkout_completed(event)
    assert parsed["user_id"] == 42
    assert parsed["product"] == "ai_subscription"


def test_platform_v2_auth_lawyers_webhook_countries(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "v2.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")
    monkeypatch.setattr(config, "STRIPE_SECRET_KEY", "")
    monkeypatch.setattr(config, "STRIPE_WEBHOOK_SECRET", "")
    monkeypatch.setenv("STRIPE_SECRET_KEY", "")
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", "")
    monkeypatch.setenv("ALLOW_MOCK_BILLING", "true")

    with TestClient(server.app) as client:
        meta = client.get("/api/meta")
        assert meta.status_code == 200
        assert meta.json()["version"].startswith("2.")
        assert meta.json()["database_backend"] == "sqlite"

        session = client.post("/api/auth/session", json={"user_id": 777})
        assert session.status_code == 200
        token = session.json()["token"]
        me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me.status_code == 200
        assert me.json()["user"]["user_id"] == 777

        magic = client.post(
            "/api/auth/magic-link",
            json={"user_id": 777, "email": "demo@example.com"},
        )
        assert magic.status_code == 200
        assert magic.json().get("claim_url")

        lawyers = client.get("/api/lawyers")
        assert lawyers.status_code == 200
        lawyer_id = lawyers.json()[0]["id"]
        lead = client.post(
            "/api/lawyers/leads",
            json={
                "user_id": 777,
                "lawyer_id": lawyer_id,
                "contact": "@demo",
                "message": "Potrzebuję pomocy z kartą pobytu",
            },
        )
        assert lead.status_code == 200
        assert lead.json()["ok"] is True

        countries = client.get("/api/countries")
        assert countries.status_code == 200
        assert countries.json()["default"] == "pl"

        webhook = client.post(
            "/api/billing/webhook",
            json={
                "type": "checkout.session.completed",
                "data": {
                    "object": {
                        "id": "cs_test_v2",
                        "metadata": {
                            "user_id": "777",
                            "product": "ai_subscription",
                        },
                        "payment_status": "paid",
                    }
                },
            },
        )
        assert webhook.status_code == 200
        assert webhook.json()["handled"] is True

        cabinet = client.get("/api/cabinet/777")
        assert cabinet.status_code == 200
        assert cabinet.json()["plan"]["unlimited"] is True

        admin_page = client.get("/admin")
        assert admin_page.status_code == 200

        health = client.get("/health")
        assert health.status_code == 200
        assert health.json()["status"] == "ok"
        ready = client.get("/ready")
        assert ready.status_code == 200
        assert "ocr" in ready.json()
        assert "mock_billing_allowed" in ready.json()
