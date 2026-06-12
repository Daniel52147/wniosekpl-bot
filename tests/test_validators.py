from src.validators import validate_field


def test_date_ok():
    assert validate_field("data_urodzenia", "15.03.1990", "ru") is None


def test_date_bad():
    assert validate_field("data_urodzenia", "99.99.9999", "ru") is not None


def test_required_empty():
    assert validate_field("imie", "", "ru") is not None


def test_optional_empty():
    assert validate_field("imie_ojca", "", "ru") is None


def test_pesel_brak():
    assert validate_field("pesel", "brak", "ru") is None


def test_data_od():
    assert validate_field("data_od", "01.01.2025", "en") is None
    assert validate_field("data_od", "bad", "en") is not None
