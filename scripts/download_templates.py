"""Pobierz oficjalne PDF z gov.pl."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.templates_loader import ensure_official_templates


def main() -> int:
    for name in ensure_official_templates(force=True):
        size = (ROOT / "templates" / "official" / name).stat().st_size
        print(f"OK {name} ({size} bytes)")
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
