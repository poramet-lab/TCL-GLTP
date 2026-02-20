#!/usr/bin/env python3
from __future__ import annotations

import json
import logging
import signal
import sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from tci_gltp.config import DB_PATH, ROOT, SESSION_ROOTS

WEB_ROOT = ROOT / "web"
MAX_LIMIT = 500
DEFAULT_LIMIT = 100
MAX_MESSAGES_PER_SESSION = 3000

log = logging.getLogger(__name__)


def _escape_like(value: str) -> str:
    """Escape special LIKE characters so they match literally."""
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def _db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _validate_owner_limit(q: dict, handler: Handler) -> tuple[str, int] | None:
    """Validate owner and limit params. Returns (owner, limit) or None on error."""
    owner = (q.get("owner") or [""])[0].strip()
    limit = handler._parse_limit((q.get("limit") or [None])[0])
    if limit is None:
        handler._error("INVALID_LIMIT", f"limit must be a positive integer (1-{MAX_LIMIT})")
        return None
    if owner and owner not in SESSION_ROOTS:
        allowed = ", ".join(sorted(SESSION_ROOTS.keys()))
        handler._error("INVALID_OWNER", f"owner must be one of: {allowed}")
        return None
    return owner, limit


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_ROOT), **kwargs)

    def _json(self, obj: object, status: int = 200) -> None:
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, code: str, message: str, status: int = 400) -> None:
        return self._json({"error": {"code": code, "message": message}}, status=status)

    def _parse_limit(self, raw: str | None) -> int | None:
        if raw is None or raw == "":
            return DEFAULT_LIMIT
        try:
            value = int(raw)
        except ValueError:
            return None
        if value <= 0:
            return None
        return min(value, MAX_LIMIT)

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/health":
            return self._json({"ok": True})

        if parsed.path == "/api/owners":
            return self._json(sorted(SESSION_ROOTS.keys()))

        if parsed.path == "/api/sessions":
            q = parse_qs(parsed.query)
            result = _validate_owner_limit(q, self)
            if result is None:
                return
            owner, limit = result
            where, params = "", []
            if owner:
                where = "WHERE owner = ?"
                params.append(owner)
            params.append(limit)
            with _db() as conn:
                rows = conn.execute(
                    f"""
                    SELECT session_id, owner, started_at_bkk, ended_at_bkk, message_count
                    FROM sessions
                    {where}
                    ORDER BY COALESCE(ended_at_utc, '') DESC
                    LIMIT ?
                    """,
                    params,
                ).fetchall()
            return self._json([dict(r) for r in rows])

        if parsed.path == "/api/search_messages":
            q = parse_qs(parsed.query)
            result = _validate_owner_limit(q, self)
            if result is None:
                return
            owner, limit = result
            keyword = (q.get("q") or [""])[0].strip()
            if not keyword:
                return self._error("MISSING_QUERY", "q is required")
            like = f"%{_escape_like(keyword)}%"
            where_parts = ["m.text LIKE ? ESCAPE '\\'"]
            params: list[str | int] = [like]
            if owner:
                where_parts.append("s.owner = ?")
                params.append(owner)
            params.append(limit)
            where_clause = " AND ".join(where_parts)
            with _db() as conn:
                rows = conn.execute(
                    f"""
                    SELECT
                      s.session_id,
                      s.owner,
                      s.started_at_bkk,
                      s.ended_at_bkk,
                      s.message_count,
                      COUNT(m.message_id) AS hit_count
                    FROM messages m
                    JOIN sessions s ON s.session_id = m.session_id
                    WHERE {where_clause}
                    GROUP BY s.session_id, s.owner, s.started_at_bkk, s.ended_at_bkk, s.message_count, s.ended_at_utc
                    ORDER BY hit_count DESC, COALESCE(s.ended_at_utc, '') DESC
                    LIMIT ?
                    """,
                    params,
                ).fetchall()
            return self._json([dict(r) for r in rows])

        if parsed.path == "/api/messages":
            q = parse_qs(parsed.query)
            session_id = (q.get("session_id") or [""])[0].strip()
            if not session_id:
                return self._error("MISSING_SESSION_ID", "session_id is required")
            with _db() as conn:
                rows = conn.execute(
                    """
                    SELECT ts_bkk, role, text
                    FROM messages
                    WHERE session_id = ?
                    ORDER BY ts_utc ASC
                    LIMIT ?
                    """,
                    (session_id, MAX_MESSAGES_PER_SESSION),
                ).fetchall()
            return self._json([dict(r) for r in rows])

        return super().do_GET()


def main() -> int:
    import argparse

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8020)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)

    def _shutdown_handler(signum: int, _frame: object) -> None:
        log.info("received signal %s, shutting down server", signum)
        server.shutdown()

    signal.signal(signal.SIGTERM, _shutdown_handler)
    signal.signal(signal.SIGINT, _shutdown_handler)

    log.info("TCI-GLTP API+Web: http://%s:%d/", args.host, args.port)
    server.serve_forever()
    log.info("server stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
