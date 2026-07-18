from src.ai_assistant import answer_question


def test_ai_assistant_answers_karta_pobytu_question():
    answer = answer_question(
        "Я гражданин Украины. Работаю официально. Хочу получить карту побыту.",
        "ru",
    )

    assert answer.topic == "karta_pobytu"
    assert "Karta pobytu" in answer.text
    assert "не юридическая консультация" in answer.text
    assert any(a["type"] == "goto" and a["id"] == "mos" for a in answer.actions)
    assert "/docs" not in answer.text


def test_ai_assistant_pesel_has_open_doc_action():
    answer = answer_question("Jak dostać PESEL?", "pl")
    assert answer.topic == "pesel"
    assert any(a["type"] == "open_doc" and a["id"] == "pesel" for a in answer.actions)
    assert "Przycisk" in answer.text or "przycisk" in answer.text.lower()


def test_ai_assistant_answers_office_letter_question():
    answer = answer_question("Dostałem wezwanie z urzędu, co robić?", "pl")

    assert answer.topic == "office_letter"
    assert "Pismo z urzędu" in answer.text
    assert any(a["id"] == "pismo_do_urzedu" for a in answer.actions)


def test_ai_assistant_fallback_keeps_user_in_scope():
    answer = answer_question("What is the weather today?", "en")

    assert answer.topic == "fallback"
    assert "paperwork in Poland" in answer.text
    assert answer.actions


def test_assistant_api_returns_actions(tmp_path, monkeypatch):
    from fastapi.testclient import TestClient

    import server
    import src.database as database

    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "ai.db")
    monkeypatch.setattr("src.runtime_secrets.SECRETS_PATH", tmp_path / "secrets.env")

    with TestClient(server.app) as client:
        res = client.post(
            "/api/assistant/ask",
            json={"user_id": 77, "question": "Jak dostać PESEL?", "lang": "pl"},
        )
        assert res.status_code == 200
        body = res.json()
        assert body["actions"]
        assert body["actions"][0]["type"] in {"open_doc", "goto"}
        resume = client.get("/api/resume", params={"lang": "pl", "user_id": 77})
        assert resume.status_code == 200
        assert "mos_next" in resume.json()
        html = client.get("/profile").text
        assert 'id="profile"' in html
        assert "profile-tabs" in html
        assert "profile.js" in html
        assert "data-profile-tab" in html
