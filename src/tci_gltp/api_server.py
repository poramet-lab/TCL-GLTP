#!/usr/bin/env python3
from __future__ import annotations

import json
import sqlite3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from tci_gltp.config import DB_PATH, ROOT

WEB_ROOT = ROOT / "web"


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

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            return self._json({"ok": True})

        if parsed.path == "/api/sessions":
            q = parse_qs(parsed.query)
            owner = (q.get("owner") or [""])[0].strip()
            limit = min(int((q.get("limit") or ["100"])[0]), 500)
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                if owner:
                    rows = conn.execute(
                        """
                        SELECT session_id, owner, started_at_bkk, ended_at_bkk, message_count
                        FROM sessions
                        WHERE owner = ?
                        ORDER BY COALESCE(ended_at_utc, '') DESC
                        LIMIT ?
                        """,
                        (owner, limit),
                    ).fetchall()
                else:
                    rows = conn.execute(
                        """
                        SELECT session_id, owner, started_at_bkk, ended_at_bkk, message_count
                        FROM sessions
                        ORDER BY COALESCE(ended_at_utc, '') DESC
                        LIMIT ?
                        """,
                        (limit,),
                    ).fetchall()
            return self._json([dict(r) for r in rows])

        if parsed.path == "/api/messages":
            q = parse_qs(parsed.query)
            session_id = (q.get("session_id") or [""])[0]
            if not session_id:
                return self._json({"error": "session_id is required"}, status=400)
            with sqlite3.connect(DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    """
                    SELECT ts_bkk, role, text
                    FROM messages
                    WHERE session_id = ?
                    ORDER BY ts_utc ASC
                    LIMIT 3000
                    """,
                    (session_id,),
                ).fetchall()
            return self._json([dict(r) for r in rows])

        return super().do_GET()


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8020)
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"TCI-GLTP API+Web: http://{args.host}:{args.port}/")
    server.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
