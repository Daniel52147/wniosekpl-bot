-- Optional Postgres schema for shared web+bot production DB.
-- Apply when DATABASE_URL points to Postgres (Render / Neon / etc.).
-- App currently uses SQLite by default; this file is the migration target.

CREATE TABLE IF NOT EXISTS users (
    telegram_id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    language TEXT DEFAULT 'ru',
    email TEXT,
    referral TEXT,
    created_at TIMESTAMPTZ NOT NULL,
    last_active_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS completions (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL REFERENCES users(telegram_id),
    document_id TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS subscriptions (
    telegram_id BIGINT PRIMARY KEY REFERENCES users(telegram_id),
    plan TEXT NOT NULL,
    status TEXT NOT NULL,
    source TEXT DEFAULT 'stripe',
    expires_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS payments (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    product TEXT NOT NULL,
    amount_pln INTEGER NOT NULL,
    status TEXT NOT NULL,
    provider TEXT NOT NULL,
    external_id TEXT,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    token_hash TEXT PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    label TEXT DEFAULT 'web',
    expires_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    last_seen_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS lawyer_leads (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    lawyer_id TEXT NOT NULL,
    contact TEXT DEFAULT '',
    message TEXT DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS calendar_events (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    title TEXT NOT NULL,
    due_at TEXT NOT NULL,
    kind TEXT DEFAULT 'custom',
    notes TEXT DEFAULT '',
    done INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS uploads (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    filename TEXT NOT NULL,
    path TEXT NOT NULL,
    extracted_text TEXT,
    explanation TEXT,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS karta_progress (
    telegram_id BIGINT PRIMARY KEY,
    steps_json TEXT NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS ai_questions (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    question TEXT NOT NULL,
    topic TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS waitlist (
    id BIGSERIAL PRIMARY KEY,
    telegram_id BIGINT NOT NULL,
    product TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    UNIQUE (telegram_id, product)
);
