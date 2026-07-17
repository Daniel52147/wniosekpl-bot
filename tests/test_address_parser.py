from src.address_parser import parse_polish_address, split_date, split_postal


def test_parse_polish_address_with_flat_number():
    addr = parse_polish_address("ul. Marszalkowska 10/5, 00-001 Warszawa")

    assert addr.ulica == "UL. MARSZALKOWSKA"
    assert addr.numer_domu == "10"
    assert addr.numer_lokalu == "5"
    assert addr.kod_pocztowy == "00-001"
    assert addr.miejscowosc == "WARSZAWA"


def test_parse_polish_address_without_flat_number():
    addr = parse_polish_address("Testowa 7, 30-001 Krakow")

    assert addr.ulica == "TESTOWA"
    assert addr.numer_domu == "7"
    assert addr.numer_lokalu == ""
    assert addr.kod_pocztowy == "30-001"
    assert addr.miejscowosc == "KRAKOW"


def test_parse_polish_address_empty_input():
    assert parse_polish_address("").raw == ""


def test_split_date_accepts_common_separators_and_pads_values():
    assert split_date("1.2.2025") == ("01", "02", "2025")
    assert split_date("01/12/2025") == ("01", "12", "2025")
    assert split_date("bad") == ("", "", "")


def test_split_postal_accepts_hyphenated_and_compact_codes():
    assert split_postal("00-001") == ("00", "001")
    assert split_postal("00001") == ("00", "001")
    assert split_postal("bad") == ("bad", "")
