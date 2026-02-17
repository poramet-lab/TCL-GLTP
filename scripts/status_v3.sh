#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_DIR="$ROOT_DIR/.run"

for name in ingest server; do
  pid_file="$RUN_DIR/${name}.pid"
  if [[ -f "$pid_file" ]]; then
    pid="$(cat "$pid_file")"
    if kill -0 "$pid" 2>/dev/null; then
      echo "$name: running pid=$pid"
    else
      echo "$name: stale pid=$pid"
    fi
  else
    echo "$name: not running"
  fi
done

echo "--- port 8020 ---"
ss -ltnp | grep ':8020' || true

echo "--- health ---"
curl -fsS http://127.0.0.1:8020/api/health || echo '{"ok":false}'
echo
