from fastapi.testclient import TestClient

import server
import src.database as database


def test_register_login_checkout_cancel(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "auth.db")

    with TestClient(server.app) as client:
        reg = client.post(
            "/api/auth/register",
            json={
                "email": "anna@example.com",
                "password": "secret123",
                "name": "Anna",
                "lang": "pl",
            },
        )
        assert reg.status_code == 200
        body = reg.json()
        assert body["user"]["email"] == "anna@example.com"
        token = body["session"]["token"]
        user_id = body["user"]["user_id"]

        bad = client.post(
            "/api/auth/login",
            json={"email": "anna@example.com", "password": "wrong-pass"},
        )
        assert bad.status_code == 401

        login = client.post(
            "/api/auth/login",
            json={"email": "anna@example.com", "password": "secret123"},
        )
        assert login.status_code == 200

        me = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert me.status_code == 200
        assert me.json()["user"]["user_id"] == user_id

        providers = client.get("/api/auth/providers")
        assert providers.status_code == 200
        assert providers.json()["password"] is True

        checkout = client.post(
            "/api/billing/checkout",
            headers={"Authorization": f"Bearer {token}"},
            json={"user_id": user_id, "product": "ai_subscription"},
        )
        assert checkout.status_code == 200
        assert "checkout_url" in checkout.json()

        paid = client.get(
            checkout.json()["checkout_url"].replace("http://testserver", ""),
            follow_redirects=False,
        )
        # mock-complete may be absolute PUBLIC_BASE_URL; call endpoint directly
        paid = client.get(
            "/api/billing/mock-complete",
            params={"user_id": user_id, "product": "ai_subscription"},
            follow_redirects=False,
        )
        assert paid.status_code in (302, 307)

        me2 = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert me2.json()["plan"]["unlimited"] is True

        invoices = client.get(
            f"/api/billing/invoices/{user_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert invoices.status_code == 200
        assert any(i["status"] == "paid" for i in invoices.json()["items"])

        cancel = client.post(
            "/api/billing/cancel",
            headers={"Authorization": f"Bearer {token}"},
            json={"user_id": user_id},
        )
        assert cancel.status_code == 200
        assert cancel.json()["ok"] is True


def test_password_reset_flow(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "reset.db")
    with TestClient(server.app) as client:
        client.post(
            "/api/auth/register",
            json={
                "email": "reset@example.com",
                "password": "oldpass123",
                "name": "Reset",
            },
        )
        forgot = client.post(
            "/api/auth/password/forgot",
            json={"email": "reset@example.com"},
        )
        assert forgot.status_code == 200
        reset_url = forgot.json()["reset_url"]
        token = reset_url.split("reset_token=")[1].split("#")[0]
        reset = client.post(
            "/api/auth/password/reset",
            json={"token": token, "password": "newpass123"},
        )
        assert reset.status_code == 200
        login = client.post(
            "/api/auth/login",
            json={"email": "reset@example.com", "password": "newpass123"},
        )
        assert login.status_code == 200


def test_duplicate_email_rejected(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "dup.db")
    with TestClient(server.app) as client:
        payload = {
            "email": "dup@example.com",
            "password": "secret123",
            "name": "A",
        }
        assert client.post("/api/auth/register", json=payload).status_code == 200
        again = client.post("/api/auth/register", json=payload)
        assert again.status_code == 400
        assert again.json()["detail"] == "email_taken"
