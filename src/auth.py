"""Web session tokens so users are not only anonymous numeric IDs."""

from __future__ import annotations

import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from src.database import (
    create_session,
    get_session,
    revoke_session,
    touch_session,
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def new_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


async def issue_session(user_id: int, *, days: int = 30, label: str = "web") -> dict:
    token = new_token()
    expires = (_now() + timedelta(days=days)).isoformat()
    await create_session(hash_token(token), user_id, expires, label)
    return {
        "token": token,
        "user_id": user_id,
        "expires_at": expires,
        "label": label,
    }


def extract_bearer(token: str | None) -> str | None:
    if not token:
        return None
    raw = token.strip()
    if raw.lower().startswith("bearer "):
        raw = raw[7:].strip()
    return raw or None


async def resolve_session(token: str | None) -> int | None:
    raw = extract_bearer(token)
    if not raw:
        return None
    row = await get_session(hash_token(raw))
    if not row:
        return None
    expires = row.get("expires_at") or ""
    if expires and expires < _now().isoformat():
        return None
    await touch_session(row["token_hash"])
    return int(row["telegram_id"])


async def logout_session(token: str | None) -> bool:
    raw = extract_bearer(token)
    if not raw:
        return False
    return await revoke_session(hash_token(raw))
