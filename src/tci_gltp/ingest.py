#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

from tci_gltp.config import DB_PATH, SESSION_ROOTS
from tci_gltp.db import connect, init_schema

TZ_BKK = ZoneInfo("Asia/Bangkok")
SCHEMA_PATH = Path(__file__).with_name("schema.sql")


def to_bkk(ts: str) -> str:
    dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return dt.astimezone(TZ_BKK).strftime("%Y-%m-%d %H:%M:%S +07")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def iter_source_files() -> list[tuple[str, Path, Path]]:
    out: list[tuple[str, Path, Path]] = []
    for owner, root in SESSION_ROOTS.items():
        if not root.exists():
            continue
        for p in sorted(root.rglob("*.jsonl")):
            out.append((owner, root, p))
    return out


def msg_id(session_id: str, ts: str, role: str, text: str) -> str:
    key = f"{session_id}|{ts}|{role}|{text}".encode("utf-8")
    return hashlib.sha1(key).hexdigest()


def parse_messages(owner: str, source_file: Path, session_id: str) -> list[tuple[str, str, str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str, str, str]] = []
    with source_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") != "event_msg":
                continue
            payload = obj.get("payload") or {}
            kind = payload.get("type")
            if kind not in {"user_message", "agent_message"}:
                continue
            text = (payload.get("message") or "").strip()
            ts = obj.get("timestamp")
            if not text or not ts:
                continue
            role = "USER" if kind == "user_message" else "AI"
            rows.append((
                msg_id(session_id, ts, role, text),
                session_id,
                owner,
                ts,
                to_bkk(ts),
                role,
                text,
            ))
    return rows


def upsert_session(conn: sqlite3.Connection, session_row: tuple) -> None:
    conn.execute(
        """
        INSERT INTO sessions(
          session_id, owner, source_path, started_at_utc, ended_at_utc,
          started_at_bkk, ended_at_bkk, message_count, updated_at_utc
        ) VALUES(?,?,?,?,?,?,?,?,?)
        ON CONFLICT(session_id) DO UPDATE SET
          started_at_utc=excluded.started_at_utc,
          ended_at_utc=excluded.ended_at_utc,
          started_at_bkk=excluded.started_at_bkk,
          ended_at_bkk=excluded.ended_at_bkk,
          message_count=excluded.message_count,
          updated_at_utc=excluded.updated_at_utc,
          source_path=excluded.source_path
        """,
        session_row,
    )


def ingest_once() -> tuple[int, int]:
    conn = connect(DB_PATH)
    init_schema(conn, SCHEMA_PATH)

    sessions = 0
    messages = 0

    for owner, root, source_file in iter_source_files():
        rel = source_file.relative_to(root)
        session_id = f"{owner}/{rel.as_posix()}"
        msg_rows = parse_messages(owner, source_file, session_id)
        if msg_rows:
            started_utc = msg_rows[0][3]
            ended_utc = msg_rows[-1][3]
            started_bkk = msg_rows[0][4]
            ended_bkk = msg_rows[-1][4]
        else:
            started_utc = ended_utc = started_bkk = ended_bkk = None

        upsert_session(
            conn,
            (
                session_id,
                owner,
                str(source_file),
                started_utc,
                ended_utc,
                started_bkk,
                ended_bkk,
                len(msg_rows),
                utc_now_iso(),
            ),
        )
        sessions += 1

        conn.executemany(
            """
            INSERT INTO messages(message_id, session_id, owner, ts_utc, ts_bkk, role, text)
            VALUES(?,?,?,?,?,?,?)
            ON CONFLICT(message_id) DO NOTHING
            """,
            msg_rows,
        )
        messages += len(msg_rows)

    conn.commit()
    conn.close()
    return sessions, messages


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--interval", type=float, default=3.0)
    args = parser.parse_args()

    if not args.watch:
        s, m = ingest_once()
        print(f"ingested sessions={s} messages={m}")
        return 0

    import time

    last_sig: tuple[tuple[str, int, int], ...] | None = None
    while True:
        sig: list[tuple[str, int, int]] = []
        for _, _, p in iter_source_files():
            st = p.stat()
            sig.append((str(p), st.st_mtime_ns, st.st_size))
        cur = tuple(sorted(sig))
        if cur != last_sig:
            s, m = ingest_once()
            print(f"watch ingest sessions={s} messages={m}")
            last_sig = cur
        time.sleep(max(0.5, args.interval))


if __name__ == "__main__":
    raise SystemExit(main())
