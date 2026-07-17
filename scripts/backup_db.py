"""Backup the configured SQLite database."""
import shutil
from datetime import datetime
from pathlib import Path

from src.config import DATABASE_PATH


def backup_database(
    src: Path = DATABASE_PATH,
    dest_dir: Path | None = None,
    stamp: str | None = None,
) -> Path | None:
    src = Path(src)
    if not src.exists():
        return None

    dest_dir = Path(dest_dir) if dest_dir else src.parent / "backups"
    dest_dir.mkdir(parents=True, exist_ok=True)

    stamp = stamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = dest_dir / f"{src.stem}_{stamp}{src.suffix}"
    shutil.copy2(src, dest)
    return dest


def main() -> None:
    dest = backup_database()
    if dest is None:
        print("No database found:", DATABASE_PATH)
        return
    print("Backup saved:", dest)


if __name__ == "__main__":
    main()
