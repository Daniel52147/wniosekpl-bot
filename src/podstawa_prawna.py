PODSTAWA_PRESETS: dict[str, dict[str, str]] = {
    "zus": {
        "pl": "art. 7 ust. 2 ustawy z dnia 27 sierpnia 2004 r. o swiadczeniach opieki zdrowotnej",
        "label_ru": "ZUS / NFZ (zdrowie)",
        "label_en": "ZUS / NFZ (healthcare)",
        "label_ua": "ZUS / NFZ",
    },
    "praca": {
        "pl": "art. 38 ust. 1a ustawy z dnia 13 pazdziernika 1998 r. o systemie ubezpieczen spolecznych",
        "label_ru": "Umowa o prace / pracodawca",
        "label_en": "Employment contract / employer",
        "label_ua": "Umowa o prace",
    },
    "uczelnia": {
        "pl": "art. 242 ust. 1 ustawy z dnia 11 lutego 2016 r. o pomocy panstwa w wychowaniu dzieci",
        "label_ru": "Uczelnia / studia (w razie wymogu urzedu)",
        "label_en": "University (if required by office)",
        "label_ua": "Uczelnia / studia",
    },
    "pobyt": {
        "pl": "art. 86 ust. 1 pkt 1 ustawy z dnia 12 grudnia 2013 r. o cudzoziemcach",
        "label_ru": "Pobyt czasowy / cudzoziemiec",
        "label_en": "Residence permit / foreigner act",
        "label_ua": "Pobyt czasowy",
    },
}


def preset_value(key: str) -> str:
    return PODSTAWA_PRESETS[key]["pl"]
