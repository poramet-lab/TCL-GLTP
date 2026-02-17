# TCI-GLTP

Team Conversation Intelligence for GLTP.

## Goal
- Aggregate multi-user Codex session logs
- Provide near-real-time team visibility
- Build analytics-ready conversation history for AI insights

## V3 Skeleton Included
- Ingestion pipeline from `.codex/sessions` for 3 owners
- SQLite schema (`sessions`, `messages`)
- API server (`/api/sessions`, `/api/messages`, `/api/health`)
- Web dashboard for browsing sessions/messages

## Project Structure
- `src/tci_gltp/` core code
- `web/` dashboard UI
- `scripts/start_v3.sh` run ingest watcher + API/web
- `scripts/stop_v3.sh` stop background services
- `data/processed/tci_gltp.sqlite3` analytics DB

## Run
```bash
cd /workspace/TCI-GLTP
./scripts/start_v3.sh
```

Open:
- `http://127.0.0.1:8020/`

Stop:
```bash
./scripts/stop_v3.sh
```

## Notes
- Timezone shown in UI is Asia/Bangkok (+07)
- ACL must allow reading all target session roots
