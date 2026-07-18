from datetime import date, timedelta

from fastapi.testclient import TestClient

from src.onboarding import build_plan
import server
import src.database as database


def test_build_plan_without_pesel():
    plan = build_plan("work", False, None, "ru")
    assert plan["first_step"] == "pesel"
    assert plan["purpose"] == "work"
    assert any("PESEL" in line for line in plan["summary_lines"])


def test_build_plan_with_pesel_and_due():
    due = (date.today() + timedelta(days=40)).isoformat()
    plan = build_plan("study", True, due, "pl")
    assert plan["first_step"] == "trusted_profile"
    assert plan["due_at"] == due
    assert any("Profil Zaufany" in line or "legalnego" in line for line in plan["summary_lines"])


def test_onboarding_api_and_profile_ui(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "ob.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    with TestClient(server.app) as client:
        copy = client.get("/api/onboarding/copy", params={"lang": "en"})
        assert copy.status_code == 200
        assert "3 questions" in copy.json()["copy"]["title"].lower() or "question" in copy.json()["copy"]["title"].lower()

        due = (date.today() + timedelta(days=30)).isoformat()
        res = client.post(
            "/api/onboarding",
            json={
                "user_id": 555,
                "purpose": "work",
                "has_pesel": True,
                "due_at": due,
                "lang": "pl",
            },
        )
        assert res.status_code == 200
        body = res.json()
        assert body["ok"] is True
        assert body["steps"].get("pesel") is True
        assert body["steps"].get("legal_stay") is True
        assert body["next_action"]["id"] != "pesel"
        assert body["event_id"]

        html = client.get("/profile").text
        assert 'id="onboarding"' in html
        assert "onboarding.js" in html
        assert 'id="ob-purposes"' in html
