"""Backup SQLite database to data/backups/."""
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "urzad.db"
DEST_DIR = ROOT / "data" / "backups"


def main() -> None:
    if not SRC.exists():
        print("No database found:", SRC)
        return
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = DEST_DIR / f"urzad_{stamp}.db"
    shutil.copy2(SRC, dest)
    print("Backup saved:", dest)


if __name__ == "__main__":
    main()
