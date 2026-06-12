import re
from dataclasses import dataclass


@dataclass
class ParsedAddress:
    ulica: str = ""
    numer_domu: str = ""
    numer_lokalu: str = ""
    kod_pocztowy: str = ""
    miejscowosc: str = ""
    raw: str = ""


_POSTAL_RE = re.compile(r"\b(\d{2}-\d{3})\b")
_HOUSE_RE = re.compile(r"(\d+[A-Za-z]?)(?:/(\d+[A-Za-z]?))?\s*$")


def _split_street_and_number(street_part: str) -> tuple[str, str, str]:
    street_part = street_part.strip()
    m = _HOUSE_RE.search(street_part)
    if not m:
        return street_part, "", ""
    return (
        street_part[: m.start()].strip(),
        m.group(1),
        m.group(2) or "",
    )


def parse_polish_address(text: str) -> ParsedAddress:
    """Best-effort split of free-text address (ulica, nr, kod, miasto)."""
    raw = (text or "").strip()
    if not raw:
        return ParsedAddress(raw=raw)

    kod = ""
    m = _POSTAL_RE.search(raw)
    if m:
        kod = m.group(1)

    without_postal = _POSTAL_RE.sub("", raw).strip(" ,;")
    parts = [p.strip() for p in re.split(r"[,;]", without_postal) if p.strip()]

    ulica = ""
    numer_domu = ""
    numer_lokalu = ""
    miejscowosc = ""

    if len(parts) >= 2:
        ulica, numer_domu, numer_lokalu = _split_street_and_number(parts[0])
        miejscowosc = parts[-1]
    elif len(parts) == 1:
        ulica, numer_domu, numer_lokalu = _split_street_and_number(parts[0])
        if kod:
            tail = raw.split(kod, 1)[-1].strip(" ,;-")
            miejscowosc = tail

    if kod and not miejscowosc:
        miejscowosc = raw.split(kod, 1)[-1].strip(" ,;-")

    return ParsedAddress(
        ulica=ulica.upper(),
        numer_domu=numer_domu,
        numer_lokalu=numer_lokalu,
        kod_pocztowy=kod,
        miejscowosc=miejscowosc.upper(),
        raw=raw,
    )


def split_date(value: str) -> tuple[str, str, str]:
    """DD.MM.RRRR -> day, month, year strings."""
    value = (value or "").strip()
    m = re.match(r"(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})", value)
    if not m:
        return "", "", ""
    d, mo, y = m.group(1), m.group(2), m.group(3)
    return d.zfill(2), mo.zfill(2), y


def split_postal(kod: str) -> tuple[str, str]:
    kod = (kod or "").strip()
    if "-" in kod:
        a, b = kod.split("-", 1)
        return a, b
    if len(kod) == 5:
        return kod[:2], kod[2:]
    return kod, ""
