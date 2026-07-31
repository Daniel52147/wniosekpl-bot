from fastapi.testclient import TestClient

import server
import src.config as config
import src.database as database


def test_wakacje_promo_grants_one_month(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "promo.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")
    monkeypatch.setattr(config, "STRIPE_SECRET_KEY", "")
    monkeypatch.setenv("STRIPE_SECRET_KEY", "")

    with TestClient(server.app) as client:
        reg = client.post(
            "/api/auth/register",
            json={
                "email": "promo@example.com",
                "password": "secret123",
                "name": "Promo",
                "lang": "pl",
            },
        )
        assert reg.status_code == 200
        token = reg.json()["session"]["token"]
        user_id = reg.json()["user"]["user_id"]

        bad = client.post(
            "/api/billing/promo",
            headers={"Authorization": f"Bearer {token}"},
            json={"user_id": user_id, "code": "NOPE"},
        )
        assert bad.status_code == 400

        ok = client.post(
            "/api/billing/promo",
            headers={"Authorization": f"Bearer {token}"},
            json={"user_id": user_id, "code": "wakacje"},
        )
        assert ok.status_code == 200
        body = ok.json()
        assert body["ok"] is True
        assert body["days"] == 30
        assert body["code"] == "WAKACJE"

        me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me.status_code == 200
        assert me.json()["plan"]["unlimited"] is True

        again = client.post(
            "/api/billing/promo",
            headers={"Authorization": f"Bearer {token}"},
            json={"user_id": user_id, "code": "WAKACJE"},
        )
        assert again.status_code == 409
