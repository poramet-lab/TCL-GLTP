#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$ROOT_DIR/.run"
INGEST_PID="$RUN_DIR/ingest.pid"
SERVER_PID="$RUN_DIR/server.pid"

mkdir -p "$RUN_DIR"

cleanup_stale() {
  local f="$1"
  if [[ -f "$f" ]] && ! kill -0 "$(cat "$f")" 2>/dev/null; then
    rm -f "$f"
  fi
}

cleanup_stale "$INGEST_PID"
cleanup_stale "$SERVER_PID"

if [[ ! -f "$INGEST_PID" ]]; then
  setsid nohup env PYTHONPATH="$ROOT_DIR/src" python3 "$ROOT_DIR/src/tci_gltp/ingest.py" --watch --interval 3.0 >"$RUN_DIR/ingest.log" 2>&1 < /dev/null &
  echo $! > "$INGEST_PID"
fi

if [[ ! -f "$SERVER_PID" ]]; then
  setsid nohup env PYTHONPATH="$ROOT_DIR/src" python3 "$ROOT_DIR/src/tci_gltp/api_server.py" --port 8020 >"$RUN_DIR/server.log" 2>&1 < /dev/null &
  echo $! > "$SERVER_PID"
fi

sleep 0.5
curl -fsS http://127.0.0.1:8020/api/health >/dev/null

echo "TCI-GLTP started: http://127.0.0.1:8020/"
echo "ingest pid=$(cat "$INGEST_PID"), server pid=$(cat "$SERVER_PID")"
