PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS sessions (
  session_id TEXT PRIMARY KEY,
  owner TEXT NOT NULL,
  source_path TEXT NOT NULL,
  started_at_utc TEXT,
  ended_at_utc TEXT,
  started_at_bkk TEXT,
  ended_at_bkk TEXT,
  message_count INTEGER NOT NULL DEFAULT 0,
  updated_at_utc TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
  message_id TEXT PRIMARY KEY,
  session_id TEXT NOT NULL,
  owner TEXT NOT NULL,
  ts_utc TEXT NOT NULL,
  ts_bkk TEXT NOT NULL,
  role TEXT NOT NULL,
  text TEXT NOT NULL,
  FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);

CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
CREATE INDEX IF NOT EXISTS idx_messages_ts ON messages(ts_utc);
CREATE INDEX IF NOT EXISTS idx_messages_owner ON messages(owner);
