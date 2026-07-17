from fastapi.testclient import TestClient

import server
import src.database as database
import src.runtime_secrets as runtime_secrets


def test_setup_configure_persists_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "setup.db")
    monkeypatch.setattr(runtime_secrets, "SECRETS_PATH", tmp_path / "secrets.env")
    monkeypatch.setattr(server, "ADMIN_API_KEY", "")

    with TestClient(server.app) as client:
        status = client.get("/api/setup/status")
        assert status.status_code == 200
        assert "redirects" in status.json()

        conf = client.post(
            "/api/setup/configure",
            json={
                "keys": {
                    "STRIPE_SECRET_KEY": "sk_test_demo",
                    "GOOGLE_CLIENT_ID": "gid",
                    "GOOGLE_CLIENT_SECRET": "gsecret",
                    "PUBLIC_BASE_URL": "https://example.test",
                }
            },
        )
        assert conf.status_code == 200
        assert conf.json()["ok"] is True
        assert "STRIPE_SECRET_KEY" in conf.json()["saved_keys"]
        assert conf.json()["status"]["stripe"] is True
        assert conf.json()["status"]["google"] is True

        page = client.get("/setup")
        assert page.status_code == 200
