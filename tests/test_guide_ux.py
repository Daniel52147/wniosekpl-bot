from fastapi.testclient import TestClient

import server
import src.database as database
from src.guide_ux import guide_ux_payload


def test_guide_ux_payload_has_three_stages():
    data = guide_ux_payload("pl", "prepare")
    assert len(data["path"]) == 3
    assert data["path"][0]["id"] == "prepare"
    assert any("mos.cudzoziemcy.gov.pl" in g["url"] for g in data["official_links"])
    assert "gov.pl" in data["copy"]["official_note"] or "MOS" in data["copy"]["official_note"]
    assert len(data["copy"]["how_items"]) == 3


def test_guide_api_and_ui_hooks(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "guide.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    with TestClient(server.app) as client:
        res = client.get("/api/guide", params={"lang": "ru", "stage": "check"})
        assert res.status_code == 200
        body = res.json()
        assert body["stage"] == "check"
        assert body["copy"]["how_title"]
        assert len(body["official_links"]) >= 3

        profile = client.get("/profile").text
        assert 'id="official-bar"' in profile
        assert 'id="journey-path"' in profile
        assert 'id="how-card"' in profile
        assert "guide.js" in profile
        assert 'id="tab-now-hint"' in profile

        home = client.get("/").text
        assert 'id="landing-path"' in home
        assert 'id="official-bar"' in home
        assert "guide.js" in home
