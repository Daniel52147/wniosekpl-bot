#!/usr/bin/env bash
# Start OmniRoute AI gateway for WniosekPL (local).
# Source: https://github.com/diegosouzapw/OmniRoute
set -euo pipefail

PORT="${OMNIROUTE_PORT:-20128}"
DATA_DIR="${OMNIROUTE_DATA_DIR:-$HOME/.omniroute-wniosekpl}"
mkdir -p "$DATA_DIR"

if command -v docker >/dev/null 2>&1; then
  echo "Starting OmniRoute via Docker on :$PORT …"
  docker rm -f wniosekpl-omniroute >/dev/null 2>&1 || true
  docker run -d --name wniosekpl-omniroute --restart unless-stopped --stop-timeout 40 \
    -p "${PORT}:20128" \
    -v "${DATA_DIR}:/app/data" \
    diegosouzapw/omniroute:latest
  echo "Dashboard: http://127.0.0.1:${PORT}"
  echo "API:       http://127.0.0.1:${PORT}/v1"
  echo "Next: open dashboard → Providers → connect free provider → copy API key"
  echo "Then set in .env:"
  echo "  OMNIROUTE_ENABLED=true"
  echo "  OMNIROUTE_BASE_URL=http://127.0.0.1:${PORT}/v1"
  echo "  OMNIROUTE_API_KEY=<from dashboard>"
  exit 0
fi

if command -v npx >/dev/null 2>&1; then
  echo "Docker not found — starting OmniRoute via npx (Node)…"
  export PORT
  export DATA_DIR
  export INITIAL_PASSWORD="${OMNIROUTE_INITIAL_PASSWORD:-CHANGEME}"
  if [[ -z "${JWT_SECRET:-}" ]]; then
    export JWT_SECRET
    JWT_SECRET="$(openssl rand -base64 48 2>/dev/null || head -c 48 /dev/urandom | base64)"
  fi
  if [[ -z "${API_KEY_SECRET:-}" ]]; then
    export API_KEY_SECRET
    API_KEY_SECRET="$(openssl rand -hex 32 2>/dev/null || head -c 32 /dev/urandom | xxd -p -c 32)"
  fi
  exec npx --yes omniroute@latest
fi

echo "Need Docker or Node/npm to run OmniRoute."
echo "Install: https://github.com/diegosouzapw/OmniRoute#quick-start"
exit 1
