from src.documents import load_all_documents


def test_polish_questions_use_label_not_russian():
    docs = load_all_documents()
    pesel = docs["pesel"]
    imie = next(f for f in pesel.fields if f.key == "imie")
    q_pl = imie.question("pl")
    assert "Podaj" in q_pl or "Imi?" in q_pl
    assert "???????" not in q_pl.lower()


def test_polish_description():
    docs = load_all_documents()
    desc = docs["pesel"].description("pl")
    assert "gov.pl" in desc or "formularz" in desc.lower()
