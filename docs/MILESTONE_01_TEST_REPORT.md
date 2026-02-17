# Milestone 01 Test Report

วันที่ทดสอบ: 2026-02-17 13:09:43 +0700
สภาพแวดล้อม: `/workspace/TCI-GLTP`

## Test Steps and Results
1. Start services
- Command: `./scripts/start_v3.sh`
- Result: PASS

2. Runtime status
- Command: `./scripts/status_v3.sh`
- Result: PASS (ingest/server running, port `8020` listening, health ok)

3. Health endpoint
- Command: `curl -s http://127.0.0.1:8020/api/health`
- Result: PASS
- Response: `{"ok": true}`

4. Sessions endpoint (valid)
- Command: `curl -s 'http://127.0.0.1:8020/api/sessions?limit=2'`
- Result: PASS
- Response: JSON array with session objects

5. Sessions endpoint (invalid limit)
- Command: `curl -s 'http://127.0.0.1:8020/api/sessions?limit=abc'`
- Result: PASS
- Response:
```json
{"error":{"code":"INVALID_LIMIT","message":"limit must be a positive integer (1-500)"}}
```

6. Sessions endpoint (invalid owner)
- Command: `curl -s 'http://127.0.0.1:8020/api/sessions?owner=unknown'`
- Result: PASS
- Response:
```json
{"error":{"code":"INVALID_OWNER","message":"owner must be one of: first, poramet, support"}}
```

7. Messages endpoint (missing session_id)
- Command: `curl -s 'http://127.0.0.1:8020/api/messages'`
- Result: PASS
- Response:
```json
{"error":{"code":"MISSING_SESSION_ID","message":"session_id is required"}}
```

## Summary
- Smoke test ผ่านตามขอบเขต M01
- API validation และ error format มาตรฐานทำงานถูกต้อง
