# Milestone 01 Execution Plan

## Objective
Stabilize the V3 foundation so the team can use it daily for live visibility and reliable history lookup.

## In Scope
1. Ingestion stability for all configured users
2. API reliability and predictable response shape
3. Dashboard usability for daily operation
4. Operational scripts for start/stop/status
5. Baseline governance notes (ACL and data handling)

## Work Packages
1. Data Ingestion
- Validate all source roots are readable
- Add ingestion counters in logs (sessions/messages)
- Ensure re-run safety (no duplicated messages)

2. API Contract
- Confirm endpoint behavior and default limits
- Add lightweight error responses for invalid params
- Document sample responses

3. Dashboard
- Keep owner filter and session/message navigation fast
- Maintain periodic refresh when tab is active
- Ensure mobile width does not break core usage

4. Operations
- Start script launches watcher + API server
- Stop script cleanly stops both processes
- Status script reports PID, port, and health endpoint

5. Governance Baseline
- Confirm ACL read access for all target users
- Keep raw source untouched; process into analytics DB only
- Keep logs and DB paths explicit and auditable

## Definition of Done
- `./scripts/start_v3.sh` starts successfully
- `./scripts/status_v3.sh` reports healthy runtime
- Dashboard loads and can browse at least one session per owner
- `GET /api/health` returns `{ "ok": true }`
- `GET /api/sessions` and `GET /api/messages` return valid JSON

## Risks
- ACL drift causing partial ingestion visibility
- Large session files increasing ingestion latency
- Accidental process stop without monitoring

## Mitigation
- Keep status check script and quick runbook
- Use periodic manual verification until monitoring is added
- Add alerting/cron supervision in Milestone 02

## Next Milestone Preview (M02)
- Structured tagging pipeline (`project`, `intent`, `status`)
- Daily/weekly AI insight generation
- Role-based access model and retention policy
