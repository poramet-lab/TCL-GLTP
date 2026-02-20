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
  env PYTHONPATH="$ROOT_DIR/src" python3 "$ROOT_DIR/src/tci_gltp/ingest.py" --watch --interval 3.0 >>"$RUN_DIR/ingest.log" 2>&1 &
  echo $! > "$INGEST_PID"
fi

if [[ ! -f "$SERVER_PID" ]]; then
  env PYTHONPATH="$ROOT_DIR/src" python3 "$ROOT_DIR/src/tci_gltp/api_server.py" --host 127.0.0.1 --port 8020 >>"$RUN_DIR/server.log" 2>&1 &
  echo $! > "$SERVER_PID"
fi

# Wait for API server to become ready (retry up to 5 times)
for i in 1 2 3 4 5; do
  if curl -fsS http://127.0.0.1:8020/api/health >/dev/null 2>&1; then
    break
  fi
  if [[ "$i" -eq 5 ]]; then
    echo "WARNING: health check failed after 5 attempts" >&2
    exit 1
  fi
  sleep 1
done

echo "TCI-GLTP started: http://127.0.0.1:8020/"
echo "ingest pid=$(cat "$INGEST_PID"), server pid=$(cat "$SERVER_PID")"
