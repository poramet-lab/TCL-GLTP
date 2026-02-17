# API Reference (M01)

Base URL: `http://127.0.0.1:8020`

## 1) Health Check
`GET /api/health`

Response 200:
```json
{"ok": true}
```

## 2) Sessions
`GET /api/sessions?owner=<owner>&limit=<n>`

Parameters:
- `owner` (optional): `poramet` | `support` | `first`
- `limit` (optional): positive integer, default `100`, max `500`

Response 200 (example):
```json
[
  {
    "session_id": "poramet/2026/02/16/rollout-...jsonl",
    "owner": "poramet",
    "started_at_bkk": "2026-02-16 16:08:46 +07",
    "ended_at_bkk": "2026-02-17 12:32:20 +07",
    "message_count": 227
  }
]
```

Response 400 (example: invalid limit):
```json
{
  "error": {
    "code": "INVALID_LIMIT",
    "message": "limit must be a positive integer (1-500)"
  }
}
```

Response 400 (example: invalid owner):
```json
{
  "error": {
    "code": "INVALID_OWNER",
    "message": "owner must be one of: first, poramet, support"
  }
}
```

## 3) Messages
`GET /api/messages?session_id=<session_id>`

Parameters:
- `session_id` (required): full session id string from `/api/sessions`

Response 200 (example):
```json
[
  {
    "ts_bkk": "2026-02-16 16:08:46 +07",
    "role": "USER",
    "text": "..."
  },
  {
    "ts_bkk": "2026-02-16 16:08:53 +07",
    "role": "AI",
    "text": "..."
  }
]
```

Response 400 (example: missing session_id):
```json
{
  "error": {
    "code": "MISSING_SESSION_ID",
    "message": "session_id is required"
  }
}
```
