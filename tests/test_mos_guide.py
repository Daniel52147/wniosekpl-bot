from fastapi.testclient import TestClient

import server
import src.database as database
from src.mos_guide import guide_payload


def test_mos_guide_payload_has_ready_steps():
    data = guide_payload("pl")
    assert data["portal_url"].startswith("https://mos.cudzoziemcy.gov.pl")
    assert len(data["ready"]) >= 6
    assert len(data["journey"]) == 4
    assert any(p["id"] == "work" for p in data["purposes"])


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
        html = client.get("/").text
        assert 'id="mos"' in html
        assert "mos.js" in html
