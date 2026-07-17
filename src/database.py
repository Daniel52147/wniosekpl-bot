import json
from datetime import datetime, timedelta, timezone

import aiosqlite

from src.config import DATABASE_PATH


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def init_db() -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                language TEXT DEFAULT 'ru',
                created_at TEXT NOT NULL,
                last_active_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                document_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (telegram_id) REFERENCES users(telegram_id)
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS profiles (
                telegram_id INTEGER PRIMARY KEY,
                data_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                remind_at TEXT NOT NULL,
                kind TEXT DEFAULT 'meldunek',
                sent INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS waitlist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(telegram_id, product)
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS ai_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                topic TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_reminders_due
            ON reminders (sent, remind_at)
            """
        )
        await db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_completions_doc
            ON completions (document_id, created_at)
            """
        )
        await db.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_ai_questions_user_created
            ON ai_questions (telegram_id, created_at)
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS subscriptions (
                telegram_id INTEGER PRIMARY KEY,
                plan TEXT NOT NULL,
                status TEXT NOT NULL,
                source TEXT DEFAULT 'mock',
                expires_at TEXT,
                updated_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                amount_pln INTEGER NOT NULL,
                status TEXT NOT NULL,
                provider TEXT NOT NULL,
                external_id TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS calendar_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                due_at TEXT NOT NULL,
                kind TEXT DEFAULT 'custom',
                notes TEXT DEFAULT '',
                done INTEGER DEFAULT 0,
                created_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                filename TEXT NOT NULL,
                path TEXT NOT NULL,
                extracted_text TEXT,
                explanation TEXT,
                created_at TEXT NOT NULL
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS karta_progress (
                telegram_id INTEGER PRIMARY KEY,
                steps_json TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        try:
            await db.execute("ALTER TABLE users ADD COLUMN referral TEXT")
        except aiosqlite.OperationalError:
            pass
        await db.commit()


async def upsert_user(
    telegram_id: int,
    username: str | None,
    first_name: str | None,
    language: str | None = None,
) -> None:
    now = _now()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT telegram_id FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        row = await cursor.fetchone()
        if row:
            if language:
                await db.execute(
                    """
                    UPDATE users
                    SET username = ?, first_name = ?, language = ?, last_active_at = ?
                    WHERE telegram_id = ?
                    """,
                    (username, first_name, language, now, telegram_id),
                )
            else:
                await db.execute(
                    """
                    UPDATE users
                    SET username = ?, first_name = ?, last_active_at = ?
                    WHERE telegram_id = ?
                    """,
                    (username, first_name, now, telegram_id),
                )
        else:
            await db.execute(
                """
                INSERT INTO users (telegram_id, username, first_name, language, created_at, last_active_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (telegram_id, username, first_name, language or "ru", now, now),
            )
        await db.commit()


async def set_language(telegram_id: int, language: str) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET language = ?, last_active_at = ? WHERE telegram_id = ?",
            (language, _now(), telegram_id),
        )
        await db.commit()


async def set_referral(telegram_id: int, referral: str) -> None:
    ref = referral.strip()[:64]
    if not ref:
        return
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET referral = ? WHERE telegram_id = ? AND referral IS NULL",
            (ref, telegram_id),
        )
        await db.commit()


async def user_exists(telegram_id: int) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT 1 FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        return await cursor.fetchone() is not None


async def get_language(telegram_id: int) -> str:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT language FROM users WHERE telegram_id = ?",
            (telegram_id,),
        )
        row = await cursor.fetchone()
        return row[0] if row else "ru"


async def record_completion(telegram_id: int, document_id: str) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO completions (telegram_id, document_id, created_at)
            VALUES (?, ?, ?)
            """,
            (telegram_id, document_id, _now()),
        )
        await db.execute(
            "UPDATE users SET last_active_at = ? WHERE telegram_id = ?",
            (_now(), telegram_id),
        )
        await db.commit()


async def delete_user_data(telegram_id: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        for table in (
            "completions",
            "profiles",
            "reminders",
            "waitlist",
            "ai_questions",
            "subscriptions",
            "payments",
            "calendar_events",
            "uploads",
            "karta_progress",
        ):
            await db.execute(
                f"DELETE FROM {table} WHERE telegram_id = ?",
                (telegram_id,),
            )
        await db.execute("DELETE FROM users WHERE telegram_id = ?", (telegram_id,))
        await db.commit()


async def save_profile(telegram_id: int, data: dict) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO profiles (telegram_id, data_json, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                data_json = excluded.data_json,
                updated_at = excluded.updated_at
            """,
            (telegram_id, json.dumps(data, ensure_ascii=False), _now()),
        )
        await db.commit()


async def get_profile(telegram_id: int) -> dict | None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute(
            "SELECT data_json FROM profiles WHERE telegram_id = ?",
            (telegram_id,),
        )
        row = await cur.fetchone()
        if not row:
            return None
        return json.loads(row[0])


async def add_reminder(telegram_id: int, remind_at: str, kind: str = "meldunek") -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO reminders (telegram_id, remind_at, kind, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (telegram_id, remind_at, kind, _now()),
        )
        await db.commit()


async def fetch_due_reminders() -> list[dict]:
    now = _now()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """
            SELECT r.id, r.telegram_id, u.language as lang
            FROM reminders r
            LEFT JOIN users u ON u.telegram_id = r.telegram_id
            WHERE r.sent = 0 AND r.remind_at <= ?
            """,
            (now,),
        )
        rows = await cur.fetchall()
        return [dict(row) for row in rows]


async def mark_reminder_sent(reminder_id: int) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE reminders SET sent = 1 WHERE id = ?",
            (reminder_id,),
        )
        await db.commit()


async def join_waitlist(telegram_id: int, product: str) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        try:
            await db.execute(
                """
                INSERT INTO waitlist (telegram_id, product, created_at)
                VALUES (?, ?, ?)
                """,
                (telegram_id, product, _now()),
            )
            await db.commit()
            return True
        except aiosqlite.IntegrityError:
            return False


async def waitlist_count(product: str) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute(
            "SELECT COUNT(*) FROM waitlist WHERE product = ?",
            (product,),
        )
        return (await cur.fetchone())[0]


async def save_feedback(telegram_id: int, message: str) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO feedback (telegram_id, message, created_at)
            VALUES (?, ?, ?)
            """,
            (telegram_id, message[:2000], _now()),
        )
        await db.commit()


async def feedback_count() -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM feedback")
        return (await cur.fetchone())[0]


async def ai_questions_today(telegram_id: int) -> int:
    day_start = datetime.now(timezone.utc).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    ).isoformat()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute(
            """
            SELECT COUNT(*)
            FROM ai_questions
            WHERE telegram_id = ? AND created_at >= ?
            """,
            (telegram_id, day_start),
        )
        return (await cur.fetchone())[0]


async def record_ai_question(telegram_id: int, question: str, topic: str) -> None:
    now = _now()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO ai_questions (telegram_id, question, topic, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (telegram_id, question[:2000], topic[:64], now),
        )
        await db.execute(
            "UPDATE users SET last_active_at = ? WHERE telegram_id = ?",
            (now, telegram_id),
        )
        await db.commit()


async def get_stats() -> dict:
    week_ago = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM users")
        users = (await cur.fetchone())[0]
        cur = await db.execute(
            "SELECT COUNT(*) FROM users WHERE created_at >= ?",
            (week_ago,),
        )
        users_7d = (await cur.fetchone())[0]
        cur = await db.execute("SELECT COUNT(*) FROM completions")
        completions = (await cur.fetchone())[0]
        cur = await db.execute(
            """
            SELECT document_id, COUNT(*) as c
            FROM completions GROUP BY document_id ORDER BY c DESC
            """
        )
        by_doc = await cur.fetchall()
        cur = await db.execute(
            """
            SELECT referral, COUNT(*) as c
            FROM users WHERE referral IS NOT NULL
            GROUP BY referral ORDER BY c DESC LIMIT 10
            """
        )
        by_ref = await cur.fetchall()
        cur = await db.execute(
            "SELECT COUNT(*) FROM users WHERE created_at >= ?",
            ((datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),),
        )
        users_1d = (await cur.fetchone())[0]
        cur = await db.execute("SELECT COUNT(*) FROM ai_questions")
        ai_questions = (await cur.fetchone())[0]
        cur = await db.execute(
            "SELECT COUNT(*) FROM ai_questions WHERE created_at >= ?",
            (week_ago,),
        )
        ai_questions_7d = (await cur.fetchone())[0]
        cur = await db.execute(
            "SELECT COUNT(*) FROM subscriptions WHERE status = 'active'"
        )
        active_subs = (await cur.fetchone())[0]
        cur = await db.execute(
            "SELECT COUNT(*) FROM payments WHERE status = 'paid'"
        )
        paid = (await cur.fetchone())[0]
    return {
        "users": users,
        "users_1d": users_1d,
        "users_7d": users_7d,
        "completions": completions,
        "ai_questions": ai_questions,
        "ai_questions_7d": ai_questions_7d,
        "active_subscriptions": active_subs,
        "paid_payments": paid,
        "by_document": by_doc,
        "by_referral": by_ref,
    }


async def set_subscription(
    telegram_id: int,
    plan: str,
    status: str = "active",
    source: str = "mock",
    days: int = 30,
) -> None:
    expires = (datetime.now(timezone.utc) + timedelta(days=days)).isoformat()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO subscriptions (telegram_id, plan, status, source, expires_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                plan = excluded.plan,
                status = excluded.status,
                source = excluded.source,
                expires_at = excluded.expires_at,
                updated_at = excluded.updated_at
            """,
            (telegram_id, plan, status, source, expires, _now()),
        )
        await db.commit()


async def get_subscription(telegram_id: int) -> dict | None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM subscriptions WHERE telegram_id = ?",
            (telegram_id,),
        )
        row = await cur.fetchone()
        return dict(row) if row else None


async def has_active_subscription(telegram_id: int, plan: str | None = None) -> bool:
    sub = await get_subscription(telegram_id)
    if not sub or sub.get("status") != "active":
        return False
    expires = sub.get("expires_at")
    if expires and expires < _now():
        return False
    if plan and sub.get("plan") != plan:
        return False
    return True


async def record_payment(
    telegram_id: int,
    product: str,
    amount_pln: int,
    status: str,
    provider: str,
    external_id: str | None = None,
) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute(
            """
            INSERT INTO payments
            (telegram_id, product, amount_pln, status, provider, external_id, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                telegram_id,
                product,
                amount_pln,
                status,
                provider,
                external_id,
                _now(),
            ),
        )
        await db.commit()
        return cur.lastrowid or 0


async def list_payments(telegram_id: int, limit: int = 20) -> list[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """
            SELECT * FROM payments
            WHERE telegram_id = ?
            ORDER BY id DESC LIMIT ?
            """,
            (telegram_id, limit),
        )
        return [dict(row) for row in await cur.fetchall()]


async def add_calendar_event(
    telegram_id: int,
    title: str,
    due_at: str,
    kind: str = "custom",
    notes: str = "",
) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute(
            """
            INSERT INTO calendar_events
            (telegram_id, title, due_at, kind, notes, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (telegram_id, title[:200], due_at, kind[:64], notes[:1000], _now()),
        )
        await db.commit()
        return cur.lastrowid or 0


async def list_calendar_events(telegram_id: int) -> list[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """
            SELECT * FROM calendar_events
            WHERE telegram_id = ? AND done = 0
            ORDER BY due_at ASC
            """,
            (telegram_id,),
        )
        return [dict(row) for row in await cur.fetchall()]


async def complete_calendar_event(event_id: int, telegram_id: int) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute(
            """
            UPDATE calendar_events
            SET done = 1
            WHERE id = ? AND telegram_id = ?
            """,
            (event_id, telegram_id),
        )
        await db.commit()
        return cur.rowcount > 0


async def save_upload(
    telegram_id: int,
    filename: str,
    path: str,
    extracted_text: str = "",
    explanation: str = "",
) -> int:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute(
            """
            INSERT INTO uploads
            (telegram_id, filename, path, extracted_text, explanation, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                telegram_id,
                filename[:255],
                path,
                extracted_text[:20000],
                explanation[:20000],
                _now(),
            ),
        )
        await db.commit()
        return cur.lastrowid or 0


async def list_uploads(telegram_id: int, limit: int = 20) -> list[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """
            SELECT id, filename, explanation, created_at
            FROM uploads
            WHERE telegram_id = ?
            ORDER BY id DESC LIMIT ?
            """,
            (telegram_id, limit),
        )
        return [dict(row) for row in await cur.fetchall()]


async def get_karta_progress(telegram_id: int) -> dict[str, bool]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute(
            "SELECT steps_json FROM karta_progress WHERE telegram_id = ?",
            (telegram_id,),
        )
        row = await cur.fetchone()
        if not row:
            return {}
        return json.loads(row[0])


async def set_karta_progress(telegram_id: int, steps: dict[str, bool]) -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO karta_progress (telegram_id, steps_json, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(telegram_id) DO UPDATE SET
                steps_json = excluded.steps_json,
                updated_at = excluded.updated_at
            """,
            (telegram_id, json.dumps(steps, ensure_ascii=False), _now()),
        )
        await db.commit()


async def recent_ai_questions(telegram_id: int, limit: int = 10) -> list[dict]:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """
            SELECT question, topic, created_at
            FROM ai_questions
            WHERE telegram_id = ?
            ORDER BY id DESC LIMIT ?
            """,
            (telegram_id, limit),
        )
        return [dict(row) for row in await cur.fetchall()]


async def admin_overview() -> dict:
    stats = await get_stats()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cur = await db.execute(
            "SELECT product, COUNT(*) FROM waitlist GROUP BY product"
        )
        waitlists = {row[0]: row[1] for row in await cur.fetchall()}
        cur = await db.execute(
            """
            SELECT product, COUNT(*) FROM payments
            WHERE status = 'paid' GROUP BY product
            """
        )
        paid_by_product = {row[0]: row[1] for row in await cur.fetchall()}
    stats["waitlists"] = waitlists
    stats["paid_by_product"] = paid_by_product
    return stats
