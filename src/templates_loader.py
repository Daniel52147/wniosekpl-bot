"""Oficjalne PDF — pobieranie i weryfikacja."""
import ssl
import urllib.error
import urllib.request
from pathlib import Path

from src.config import ROOT

OUT = ROOT / "templates" / "official"

URLS = {
    "pesel_gov.pdf": "https://www.gov.pl/attachment/36f4bf5c-702b-4c89-ad0d-3484a02fa913",
    "meldunek_el_zc_1.pdf": "https://samorzad.gov.pl/attachment/1875311f-f8f5-454e-b37b-8c54afcd10a7",
    "meldunek_el_zps_1.pdf": "https://www.gov.pl/attachment/fac08267-59f8-4a09-bbe5-07ac653e0eb3",
}


def _download(url: str, dest: Path) -> None:
    for ctx in (ssl.create_default_context(), ssl._create_unverified_context()):
        try:
            with urllib.request.urlopen(url, context=ctx, timeout=90) as resp:
                dest.write_bytes(resp.read())
                return
        except (ssl.SSLError, urllib.error.URLError):
            continue
    raise RuntimeError(f"Failed to download {url}")


def ensure_official_templates(force: bool = False) -> list[str]:
    OUT.mkdir(parents=True, exist_ok=True)
    fetched: list[str] = []
    for name, url in URLS.items():
        dest = OUT / name
        if dest.exists() and not force and dest.stat().st_size > 10_000:
            continue
        _download(url, dest)
        fetched.append(name)
    return fetched


def missing_templates() -> list[str]:
    return [name for name in URLS if not (OUT / name).exists()]
