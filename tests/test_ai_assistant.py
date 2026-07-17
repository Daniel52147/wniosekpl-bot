from src.ai_assistant import answer_question


def test_ai_assistant_answers_karta_pobytu_question():
    answer = answer_question(
        "Я гражданин Украины. Работаю официально. Хочу получить карту побыту.",
        "ru",
    )

    assert answer.topic == "karta_pobytu"
    assert "Karta pobytu" in answer.text
    assert "не юридическая консультация" in answer.text


def test_ai_assistant_answers_office_letter_question():
    answer = answer_question("Dostałem wezwanie z urzędu, co robić?", "pl")

    assert answer.topic == "office_letter"
    assert "Pismo z urzędu" in answer.text


def test_ai_assistant_fallback_keeps_user_in_scope():
    answer = answer_question("What is the weather today?", "en")

    assert answer.topic == "fallback"
    assert "paperwork questions in Poland" in answer.text
