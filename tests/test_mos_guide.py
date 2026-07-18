from datetime import date, timedelta

from fastapi.testclient import TestClient

import server
import src.database as database
from src.mos_guide import EMPLOYER_HELPER, guide_payload, next_action


def test_mos_guide_payload_has_ready_steps():
    data = guide_payload("pl")
    assert data["portal_url"].startswith("https://mos.cudzoziemcy.gov.pl")
    assert len(data["ready"]) >= 6
    assert len(data["journey"]) == 4
    assert len(data["walkthrough"]) >= 4
    assert data["employer_helper"]["message"]
    assert any(p["id"] == "work" for p in data["purposes"])


def test_next_action_points_to_first_incomplete():
    nxt = next_action({}, "en")
    assert nxt["id"] == "pesel"
    assert nxt["complete"] is False
    assert "PESEL" in nxt["title"]
    assert nxt["left"]
    assert nxt["time"]
    nxt2 = next_action({"pesel": True, "trusted_profile": True}, "en")
    assert nxt2["id"] == "legal_stay"
    done_map = {step["id"]: True for step in guide_payload("pl")["ready"]}
    assert next_action(done_map, "pl")["complete"] is True
    assert next_action(done_map, "pl")["id"] == "open_mos"
    assert next_action(done_map, "pl")["pct"] == 100
    assert EMPLOYER_HELPER["pl"]["title"]
    payload = guide_payload("pl")
    assert payload["copy"]["today_label"]
    assert payload["copy"]["do_items"]
    assert payload["ready"][0]["action"]


def test_mos_guide_api(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "mos.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    with TestClient(server.app) as client:
        res = client.get("/api/mos/guide", params={"lang": "ru"})
        assert res.status_code == 200
        body = res.json()
        assert "MOS" in body["copy"]["title"] or "MOS" in body["copy"]["cta"]
        assert body["lang"] == "ru"
        assert body["ready"][0]["title"]
        assert body["next_action"]["id"] == "pesel"
        assert body["walkthrough"][0]["body"]
        html = client.get("/profile").text
        assert 'id="mos-next"' in html
        assert "mos.js" in html
        assert "mos-mark-done" in html
        assert "mos-deadline-form" in html
        assert "mos-progress-fill" in html


def test_mos_step_and_deadline_api(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "mos2.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    with TestClient(server.app) as client:
        # create session for auth-less path via user_id (dev resolve)
        uid = 424242
        step = client.post(
            "/api/mos/step",
            json={"user_id": uid, "step_id": "pesel", "done": True},
        )
        assert step.status_code == 200
        assert step.json()["steps"]["pesel"] is True
        assert step.json()["next_action"]["id"] != "pesel"

        due = (date.today() + timedelta(days=30)).isoformat()
        dead = client.post(
            "/api/mos/deadline",
            json={"user_id": uid, "due_at": due, "days_before": 14},
        )
        assert dead.status_code == 200
        body = dead.json()
        assert body["ok"] is True
        assert body["event_id"]
        assert body["reminder_id"]
        assert body["steps"]["legal_stay"] is True

        guide = client.get("/api/mos/guide", params={"lang": "pl", "user_id": uid})
        assert guide.status_code == 200
        saved = guide.json().get("saved_progress") or {}
        assert saved.get("pesel") is True
        assert saved.get("legal_stay") is True
