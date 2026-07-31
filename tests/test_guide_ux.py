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
    assert data["copy"]["whats_new_title"]
    assert len(data["copy"]["whats_new_items"]) == 3
    assert data["copy"]["acc_session_title"]


def test_guide_ux_ru_uses_localized_tab_names():
    ru = guide_ux_payload("ru")
    items = " ".join(ru["copy"]["how_items"])
    assert "Teraz" not in items
    assert "Сейчас" in items
    assert "Документы" in items
    assert "Аккаунт" in items
    assert "заявление" in ru["copy"]["official_note"].lower() or "MOS" in ru["copy"]["official_note"]


def test_guide_api_and_ui_hooks(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "guide.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    with TestClient(server.app) as client:
        res = client.get("/api/guide", params={"lang": "ru", "stage": "check"})
        assert res.status_code == 200
        body = res.json()
        assert body["stage"] == "check"
        assert body["copy"]["how_title"]
        assert body["copy"]["whats_new_title"]
        assert len(body["official_links"]) >= 3

        profile = client.get("/profile").text
        assert 'id="official-bar"' in profile
        assert 'id="journey-path"' in profile
        assert 'id="how-card"' in profile
        assert 'id="whats-new"' in profile
        assert "guide.js" in profile
        assert 'id="tab-now-hint"' in profile
        assert 'role="tab"' in profile
        assert 'aria-controls="panel-now"' in profile

        home = client.get("/").text
        assert 'id="landing-path"' in home
        assert 'id="official-bar"' in home
        assert "guide.js" in home
