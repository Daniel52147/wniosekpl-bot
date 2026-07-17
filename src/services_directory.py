"""Curated directory of common offices/services for foreigners in Poland."""

SERVICES = [
    {
        "id": "uw_warszawa",
        "category": "urzad",
        "city": "Warszawa",
        "name": "Mazowiecki Urząd Wojewódzki w Warszawie",
        "address": "ul. Marszałkowska 3/5, 00-624 Warszawa",
        "url": "https://www.gov.pl/web/uw-mazowiecki",
        "notes": "Karta pobytu / sprawy cudzoziemców — sprawdź aktualny wydział i kolejkę.",
    },
    {
        "id": "usc_warszawa",
        "category": "gmina",
        "city": "Warszawa",
        "name": "Urzędy dzielnicowe m.st. Warszawy (PESEL / meldunek)",
        "address": "Adres zależy od dzielnicy zamieszkania",
        "url": "https://www.um.warszawa.pl/",
        "notes": "PESEL i meldunek załatwia urząd dzielnicy właściwy dla adresu.",
    },
    {
        "id": "zus_warszawa",
        "category": "zus",
        "city": "Warszawa",
        "name": "ZUS Oddział w Warszawie",
        "address": "ul. Senatorska 10, 00-082 Warszawa",
        "url": "https://www.zus.pl/",
        "notes": "Ubezpieczenia społeczne / zdrowotne.",
    },
    {
        "id": "nfz_warszawa",
        "category": "nfz",
        "city": "Warszawa",
        "name": "NFZ — Mazowiecki OW",
        "address": "ul. Chałubińskiego 8, 00-613 Warszawa",
        "url": "https://www.nfz-warszawa.pl/",
        "notes": "Informacja o uprawnieniach do świadczeń.",
    },
    {
        "id": "us_warszawa",
        "category": "podatki",
        "city": "Warszawa",
        "name": "Urząd Skarbowy (zależnie od adresu)",
        "address": "Właściwość według miejsca zamieszkania",
        "url": "https://www.podatki.gov.pl/",
        "notes": "PIT / NIP / rozliczenia.",
    },
    {
        "id": "uw_krakow",
        "category": "urzad",
        "city": "Kraków",
        "name": "Małopolski Urząd Wojewódzki w Krakowie",
        "address": "ul. Basztowa 22, 31-156 Kraków",
        "url": "https://www.malopolska.uw.gov.pl/",
        "notes": "Sprawy cudzoziemców / karta pobytu.",
    },
    {
        "id": "notariusz_generic",
        "category": "notariusz",
        "city": "Polska",
        "name": "Krajowa Rada Notarialna — wyszukiwarka",
        "address": "Cała Polska",
        "url": "https://www.kirp.pl/",
        "notes": "Pełnomocnictwo notarialne, gdy urząd wymaga formy szczególnej.",
    },
    {
        "id": "tlumacz_generic",
        "category": "tlumacz",
        "city": "Polska",
        "name": "Tłumacz przysięgły — lista MS",
        "address": "Cała Polska",
        "url": "https://www.gov.pl/",
        "notes": "Szukaj tłumacza przysięgłego języka dokumentu.",
    },
    {
        "id": "uw_wroclaw",
        "category": "urzad",
        "city": "Wrocław",
        "name": "Dolnośląski Urząd Wojewódzki we Wrocławiu",
        "address": "pl. Powstańców Warszawy 1, 50-153 Wrocław",
        "url": "https://www.duw.pl/",
        "notes": "Sprawy cudzoziemców / karta pobytu — Dolny Śląsk.",
    },
    {
        "id": "uw_gdansk",
        "category": "urzad",
        "city": "Gdańsk",
        "name": "Pomorski Urząd Wojewódzki w Gdańsku",
        "address": "ul. Okopowa 21/27, 80-810 Gdańsk",
        "url": "https://www.gdansk.uw.gov.pl/",
        "notes": "Sprawy cudzoziemców — województwo pomorskie.",
    },
    {
        "id": "uw_poznan",
        "category": "urzad",
        "city": "Poznań",
        "name": "Wielkopolski Urząd Wojewódzki w Poznaniu",
        "address": "al. Niepodległości 16/18, 61-713 Poznań",
        "url": "https://www.poznan.uw.gov.pl/",
        "notes": "Sprawy cudzoziemców — Wielkopolska.",
    },
    {
        "id": "pue_zus",
        "category": "zus",
        "city": "Polska",
        "name": "PUE ZUS — profil online",
        "address": "Online",
        "url": "https://www.zus.pl/pue",
        "notes": "Status składek / ubezpieczenia bez wizyty w oddziale.",
    },
]


def search_services(
    *,
    city: str | None = None,
    category: str | None = None,
    query: str | None = None,
) -> list[dict]:
    city_l = (city or "").casefold()
    cat_l = (category or "").casefold()
    q = (query or "").casefold()
    out = []
    for item in SERVICES:
        if city_l and city_l not in item["city"].casefold() and item["city"] != "Polska":
            continue
        if cat_l and cat_l not in item["category"].casefold():
            continue
        blob = f"{item['name']} {item['notes']} {item['category']} {item['city']}".casefold()
        if q and q not in blob:
            continue
        out.append(item)
    return out
