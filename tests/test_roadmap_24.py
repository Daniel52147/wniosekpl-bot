"""v2.4 roadmap: MOS finale, web drafts, account link, trust, ready."""

from datetime import date, timedelta

from fastapi.testclient import TestClient

import server
import src.database as database
from src.account_link import issue_link_code, link_telegram_with_code, mos_progress_for
from src.mos_guide import MOS_FILING_STEPS, guide_payload, ready_finale
from src.trust import trust_payload
from src.web_drafts import get_doc_draft, save_doc_draft


def test_ready_finale_has_attachments_and_five_steps():
    finale = ready_finale("work", "ru")
    assert finale["purpose"] == "work"
    assert len(finale["attachments"]) >= 2
    assert len(finale["steps"]) == 5
    assert finale["steps"][0]["n"] == 1
    assert "MOS" in finale["copy"]["cta"] or "Открыть" in finale["copy"]["cta"]
    assert len(MOS_FILING_STEPS) == 5
    payload = guide_payload("pl", done={s["id"]: True for s in guide_payload("pl")["ready"]}, purpose="study")
    assert payload["next_action"]["complete"] is True
    assert payload["finale"]["purpose"] == "study"
    assert payload["finale"]["portal_url"].startswith("https://mos.cudzoziemcy.gov.pl")


def test_trust_payload_has_faq_and_gov_links():
    data = trust_payload("en")
    assert "not a government" in data["copy"]["title"].lower() or "government" in data["copy"]["title"].lower()
    assert len(data["faq"]) == 5
    assert any("mos.cudzoziemcy.gov.pl" in g["url"] for g in data["gov_links"])
    assert "@" in data["contact_email"]


def test_mos_guide_api_includes_finale(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "finale.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    with TestClient(server.app) as client:
        res = client.get("/api/mos/guide", params={"lang": "pl", "purpose": "family"})
        assert res.status_code == 200
        body = res.json()
        assert body["finale"]["purpose"] == "family"
        assert len(body["finale"]["steps"]) == 5
        html = client.get("/profile").text
        assert 'id="mos-ready-finale"' in html
        assert "account-link.js" in html
        assert "trust.js" in html
        home = client.get("/").text
        assert 'id="trust"' in home
        assert 'id="trust-faq"' in home


def test_web_draft_api_persists(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "draft.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    with TestClient(server.app) as client:
        docs = client.get("/api/documents").json()
        doc_id = docs[0]["id"] if isinstance(docs, list) else list(docs.keys())[0]
        uid = 3_000_000_101
        save = client.post(
            f"/api/documents/{doc_id}/draft",
            json={"user_id": uid, "answers": {"imie": "Anna", "pesel": "123"}},
        )
        assert save.status_code == 200
        assert save.json()["draft"]["answers"]["imie"] == "Anna"
        got = client.get(f"/api/documents/{doc_id}/draft", params={"user_id": uid})
        assert got.status_code == 200
        assert got.json()["draft"]["answers"]["pesel"] == "123"


async def _async_link_flow():
    web_id = 3_000_000_202
    tg_id = 900001
    await database.upsert_user(web_id, None, None, "pl")
    await database.upsert_user(tg_id, "tguser", "TG", "ru")
    await database.set_mos_progress(web_id, {"pesel": True, "trusted_profile": True})
    await save_doc_draft(web_id, "pesel", {"imie": "Ola"})
    issued = await issue_link_code(web_id)
    result = await link_telegram_with_code(tg_id, issued["code"])
    assert result["ok"] is True
    merged = await mos_progress_for(tg_id)
    assert merged["pesel"] is True
    assert merged["trusted_profile"] is True
    draft = await get_doc_draft(tg_id, "pesel")
    assert draft and draft["answers"]["imie"] == "Ola"


def test_account_link_syncs_progress_and_drafts(tmp_path, monkeypatch):
    import asyncio

    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "link.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    async def run():
        await database.init_db()
        await _async_link_flow()

    asyncio.run(run())


def test_account_link_api_and_ready(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "linkapi.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    with TestClient(server.app) as client:
        uid = 3_000_000_303
        status = client.get("/api/account/link", params={"user_id": uid})
        assert status.status_code == 200
        assert status.json()["linked"] is False
        code_res = client.post("/api/account/link-code", params={"user_id": uid})
        assert code_res.status_code == 200
        body = code_res.json()
        assert len(body["code"]) == 6
        assert "t.me/" in body["deep_link"]
        assert "link_" in body["deep_link"]

        trust = client.get("/api/trust", params={"lang": "ru"})
        assert trust.status_code == 200
        assert len(trust.json()["faq"]) == 5

        ready = client.get("/ready")
        assert ready.status_code == 200
        data = ready.json()
        assert data["version"] == server.PRODUCT_VERSION
        assert "stripe_webhook_configured" in data
        assert "prod_checklist" in data
        assert "stable_domain" in data
        assert "backup_count" in data


def test_linked_mos_step_writes_both_sides(tmp_path, monkeypatch):
    import asyncio

    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "linkmos.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    async def prepare():
        await database.init_db()
        web_id = 3_000_000_404
        tg_id = 900002
        await database.upsert_user(web_id, None, None, "pl")
        await database.upsert_user(tg_id, None, None, "pl")
        issued = await issue_link_code(web_id)
        await link_telegram_with_code(tg_id, issued["code"])
        return web_id, tg_id

    web_id, tg_id = asyncio.run(prepare())

    with TestClient(server.app) as client:
        step = client.post(
            "/api/mos/step",
            json={"user_id": web_id, "step_id": "photo", "done": True},
        )
        assert step.status_code == 200
        assert step.json()["steps"]["photo"] is True

    async def check():
        assert (await database.get_mos_progress(tg_id)).get("photo") is True

    asyncio.run(check())
