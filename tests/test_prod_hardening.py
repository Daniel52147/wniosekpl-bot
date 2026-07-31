"""Prod hardening: webhook gate, shared deploy, deeper account sync, trust."""

import asyncio

from fastapi.testclient import TestClient

import server
import src.config as config
import src.database as database
from src.account_link import issue_link_code, link_telegram_with_code
from src.payments import billing_status, create_checkout_session, stripe_live_checkout_allowed
from src.trust import trust_payload


def test_stripe_checkout_blocked_without_webhook(monkeypatch):
    monkeypatch.setattr(config, "STRIPE_SECRET_KEY", "sk_test_x")
    monkeypatch.setattr(config, "STRIPE_WEBHOOK_SECRET", "")
    monkeypatch.setattr(config, "STRIPE_PRICE_AI_MONTHLY", "price_ai")
    monkeypatch.setenv("ALLOW_STRIPE_WITHOUT_WEBHOOK", "0")
    assert stripe_live_checkout_allowed() is False
    status = billing_status()
    assert "stripe_needs_webhook" in status["modes"]
    assert status["hint"]

    async def run():
        try:
            await create_checkout_session(1, "ai_subscription")
            raise AssertionError("expected webhook gate")
        except ValueError as exc:
            assert "stripe_webhook_required" in str(exc)

    asyncio.run(run())


def test_stripe_checkout_allowed_with_webhook_flag(monkeypatch):
    monkeypatch.setattr(config, "STRIPE_SECRET_KEY", "sk_test_x")
    monkeypatch.setattr(config, "STRIPE_WEBHOOK_SECRET", "")
    monkeypatch.setenv("ALLOW_STRIPE_WITHOUT_WEBHOOK", "true")
    assert stripe_live_checkout_allowed() is True


def test_ready_and_admin_backup(tmp_path, monkeypatch):
    db = tmp_path / "prod.db"
    monkeypatch.setattr(database, "DATABASE_PATH", db)
    monkeypatch.setattr(config, "DATABASE_PATH", db)
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")
    monkeypatch.setattr(config, "ADMIN_API_KEY", "test-admin")

    with TestClient(server.app) as client:
        # lifespan init_db creates a real SQLite file
        assert db.exists()
        ready = client.get("/ready").json()
        assert ready["version"] == server.PRODUCT_VERSION
        assert "prod_checklist" in ready
        assert "shared_db_hint" in ready

        bad = client.post("/api/admin/backup")
        assert bad.status_code == 401
        ok = client.post("/api/admin/backup", headers={"X-Admin-Key": "test-admin"})
        assert ok.status_code == 200
        assert ok.json()["ok"] is True
        assert (tmp_path / "backups").exists()


def test_link_merges_calendar_and_subscription(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "sync.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    async def run():
        await database.init_db()
        web_id = 3_000_000_501
        tg_id = 900501
        await database.upsert_user(web_id, None, None, "pl")
        await database.upsert_user(tg_id, "u", "T", "ru")
        await database.add_calendar_event(web_id, "Koniec pobytu", "2026-09-01", "mos_deadline")
        await database.update_subscription_record(
            web_id,
            plan="ai_subscription",
            status="active",
            source="promo",
            expires_at="2026-12-01T00:00:00+00:00",
        )
        issued = await issue_link_code(web_id)
        result = await link_telegram_with_code(tg_id, issued["code"])
        assert result["ok"] is True
        assert result["calendar_copied"] >= 1
        assert result["subscription_synced"] is True
        events = await database.list_calendar_events(tg_id)
        assert any(e["title"] == "Koniec pobytu" for e in events)
        sub = await database.get_subscription(tg_id)
        assert sub and sub["status"] == "active"

    asyncio.run(run())


def test_trust_sync_faq_and_profile_banner(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "ui.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")
    data = trust_payload("ru")
    assert any(item["id"] == "sync" for item in data["faq"])

    with TestClient(server.app) as client:
        html = client.get("/profile").text
        assert 'id="tg-link-banner"' in html
        assert "platform.js" not in html
        assert "account-link.js" in html
        home = client.get("/").text
        assert "tab=account&link=1" in home or "tab=account&amp;link=1" in home
        assert "2.4.1" in home or "WniosekPL" in home
