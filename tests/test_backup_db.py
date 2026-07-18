from scripts.backup_db import backup_database


def test_backup_database_copies_configured_database(tmp_path):
    db_path = tmp_path / "custom.db"
    db_path.write_bytes(b"sqlite data")

    backup_path = backup_database(
        src=db_path,
        dest_dir=tmp_path / "backups",
        stamp="20260717_134000",
    )

    assert backup_path == tmp_path / "backups" / "custom_20260717_134000.db"
    assert backup_path.read_bytes() == b"sqlite data"


def test_backup_database_returns_none_for_missing_source(tmp_path):
    backup_path = backup_database(src=tmp_path / "missing.db", dest_dir=tmp_path / "backups")

    assert backup_path is None
    assert not (tmp_path / "backups").exists()


def test_backup_database_prunes_old_copies(tmp_path):
    db_path = tmp_path / "app.db"
    db_path.write_bytes(b"v1")
    dest = tmp_path / "backups"
    for i in range(5):
        backup_database(src=db_path, dest_dir=dest, stamp=f"2026071{i}_120000", keep=3)
    kept = sorted(dest.glob("app_*.db"))
    assert len(kept) == 3
