# TCI-GLTP

Team Conversation Intelligence for GLTP.

## Purpose
TCI-GLTP collects Codex session conversations from multiple team users, converts them into structured data, and serves both:
- an operational viewer (near real-time)
- an analytics base for AI insight generation

## Current Scope (V3 Foundation)
- Multi-user session ingestion from `.codex/sessions`
- SQLite schema (`sessions`, `messages`)
- API endpoints for sessions/messages
- Web dashboard for browsing timeline and content
- Background watcher for automatic ingestion updates

## Repository Layout
- `src/tci_gltp/` core application
- `web/` frontend dashboard
- `scripts/start_v3.sh` start ingest watcher + API/web
- `scripts/stop_v3.sh` stop background services
- `scripts/status_v3.sh` runtime health/status check
- `data/processed/tci_gltp.sqlite3` analytics database
- `docs/` architecture and milestone docs

## Prerequisites
- Python 3.10+
- ACL permissions allowing read access to each source session root
- Linux environment (current scripts target bash)

## Configured Session Sources
Defined in `src/tci_gltp/config.py`:
- `/home/poramet/.codex/sessions`
- `/home/support/.codex/sessions`
- `/home/first/.codex/sessions`

## Run
```bash
cd /workspace/TCI-GLTP
./scripts/start_v3.sh
```

Open dashboard:
- `http://127.0.0.1:8020/`

## Stop
```bash
./scripts/stop_v3.sh
```

## Check Runtime Status
```bash
./scripts/status_v3.sh
```

## API
- `GET /api/health`
- `GET /api/sessions?owner=<owner>&limit=<n>`
- `GET /api/messages?session_id=<session_id>`

## Data Notes
- Source timestamps are UTC (`Z`)
- Display timestamps are converted to Asia/Bangkok (`+07`)
- Ingestion is idempotent (`messages` keyed by deterministic `message_id`)

## Milestone Plan
See `docs/MILESTONE_01_EXECUTION_PLAN.md` for implementation steps and Definition of Done.
