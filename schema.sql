CREATE TABLE IF NOT EXISTS interest_leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  phone TEXT NOT NULL,
  birth TEXT NOT NULL,
  address TEXT NOT NULL,
  priority TEXT NOT NULL,
  family TEXT NOT NULL DEFAULT '',
  consent_version TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
