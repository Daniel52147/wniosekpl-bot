"""Backup the configured SQLite database."""
import shutil
from datetime import datetime
from pathlib import Path

from src.config import DATABASE_PATH

# Keep the newest N backups (cron-friendly).
KEEP_BACKUPS = 14


def prune_backups(dest_dir: Path, stem: str, suffix: str, keep: int = KEEP_BACKUPS) -> int:
    backups = sorted(dest_dir.glob(f"{stem}_*{suffix}"))
    removed = 0
    for old in backups[:-keep] if keep > 0 else backups:
        try:
            old.unlink()
            removed += 1
        except OSError:
            pass
    return removed


def backup_database(
    src: Path = DATABASE_PATH,
    dest_dir: Path | None = None,
    stamp: str | None = None,
    keep: int = KEEP_BACKUPS,
) -> Path | None:
    src = Path(src)
    if not src.exists():
        return None

    dest_dir = Path(dest_dir) if dest_dir else src.parent / "backups"
    dest_dir.mkdir(parents=True, exist_ok=True)

    stamp = stamp or datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = dest_dir / f"{src.stem}_{stamp}{src.suffix}"
    shutil.copy2(src, dest)
    prune_backups(dest_dir, src.stem, src.suffix, keep=keep)
    return dest


def main() -> None:
    dest = backup_database()
    if dest is None:
        print("No database found:", DATABASE_PATH)
        return
    print("Backup saved:", dest)


if __name__ == "__main__":
    main()
