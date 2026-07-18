#!/usr/bin/env bash
# Single Render/VPS process: API + optional Telegram bot on ONE SQLite disk.
# Prefer this over separate api/bot services with different volumes.
set -euo pipefail

PORT="${PORT:-8000}"
DATA_DIR="$(dirname "${DATABASE_PATH:-./data/urzad.db}")"
mkdir -p "$DATA_DIR" "$DATA_DIR/backups"

# Nightly-ish backup while the process lives (every 12h).
(
  while true; do
    sleep 43200
    python -c "from scripts.backup_db import backup_database; print(backup_database() or 'no-db')" || true
  done
) &

if [[ -n "${BOT_TOKEN:-}" && "${BOT_TOKEN}" != *"your_telegram"* ]]; then
  echo "Starting Telegram bot alongside API (shared DATABASE_PATH)..."
  python bot.py &
  BOT_PID=$!
  trap 'kill $BOT_PID 2>/dev/null || true' EXIT
else
  echo "BOT_TOKEN not set — API only."
fi

# Startup backup so /ready shows db_backups quickly after first boot.
python -c "from scripts.backup_db import backup_database; print('backup', backup_database())" || true

exec python -m uvicorn server:app --host 0.0.0.0 --port "$PORT"
