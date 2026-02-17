# Architecture V3 (Draft)

## Layers
1. Ingest: parse jsonl sessions from multi-user sources
2. Normalize: map to canonical records
3. Store: raw + analytics tables
4. Serve: dashboard/API/search
5. Insight: scheduled AI-assisted summaries

## Security
- ACL-based access to session roots
- PII masking before analytics usage
- role-based viewer access
