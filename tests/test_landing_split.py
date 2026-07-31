from fastapi.testclient import TestClient

import server
import src.database as database


def test_landing_is_marketing_and_profile_is_app(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "split.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    with TestClient(server.app) as client:
        home = client.get("/")
        assert home.status_code == 200
        html = home.text
        assert 'href="/profile"' in html
        assert "profile-entry" in html
        assert "Co umie bot" in html or "can-do-list" in html or "visual-kicker" in html
        # marketing page should not mount the full chat workspace
        assert 'id="ask-form"' not in html
        assert 'id="messages"' not in html

        app = client.get("/profile")
        assert app.status_code == 200
        app_html = app.text
        assert 'id="ask-form"' in app_html
        assert 'id="profile"' in app_html
        assert "profile-tabs" in app_html
        assert 'data-profile-tab="now"' in app_html
        assert 'data-profile-tab="docs"' in app_html
        assert 'data-profile-tab="account"' in app_html
        assert 'data-profile-tab="billing"' not in app_html
        assert 'id="mos-next"' in app_html
        assert 'id="docs"' in app_html

        assert client.get("/app").status_code == 200
