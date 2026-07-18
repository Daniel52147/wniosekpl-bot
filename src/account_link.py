"""Link web account ↔ Telegram so MOS progress and drafts stay one."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone

from src.config import BOT_USERNAME
from src.database import (
    claim_link_code,
    create_link_code,
    get_link_status,
    get_linked_peer,
    get_mos_progress,
    set_mos_progress,
    unlink_accounts,
)
from src.web_drafts import merge_web_drafts

CODE_TTL_MINUTES = 15


def _now() -> datetime:
    return datetime.now(timezone.utc)


def deep_link_for(code: str) -> str:
    bot = (BOT_USERNAME or "wniosekpl_bot").lstrip("@")
    return f"https://t.me/{bot}?start=link_{code}"


async def issue_link_code(web_user_id: int) -> dict:
    """Create a one-time code for the logged-in web user."""
    # Prefer short numeric codes that are easy to type in Telegram.
    code = f"{secrets.randbelow(1_000_000):06d}"
    expires = (_now() + timedelta(minutes=CODE_TTL_MINUTES)).isoformat()
    await create_link_code(code, web_user_id, expires)
    return {
        "code": code,
        "expires_at": expires,
        "ttl_minutes": CODE_TTL_MINUTES,
        "deep_link": deep_link_for(code),
        "bot_username": (BOT_USERNAME or "wniosekpl_bot").lstrip("@"),
    }


async def _merge_progress(a: int, b: int) -> dict[str, bool]:
    left = await get_mos_progress(a)
    right = await get_mos_progress(b)
    merged = {**left}
    for key, value in right.items():
        if value:
            merged[key] = True
    await set_mos_progress(a, merged)
    await set_mos_progress(b, merged)
    return merged


async def link_telegram_with_code(telegram_id: int, code: str) -> dict:
    """Telegram side: claim code and sync progress + drafts both ways."""
    cleaned = (code or "").strip().replace("link_", "")
    web_user_id = await claim_link_code(cleaned, telegram_id)
    if web_user_id is None:
        return {"ok": False, "error": "invalid_or_expired"}
    if web_user_id == telegram_id:
        return {"ok": False, "error": "same_account"}
    steps = await _merge_progress(web_user_id, telegram_id)
    await merge_web_drafts(web_user_id, telegram_id)
    await merge_web_drafts(telegram_id, web_user_id)
    return {
        "ok": True,
        "web_user_id": web_user_id,
        "telegram_id": telegram_id,
        "steps": steps,
    }


async def status_for(user_id: int) -> dict:
    row = await get_link_status(user_id)
    peer = await get_linked_peer(user_id)
    return {
        "linked": peer is not None,
        "peer_id": peer,
        "web_user_id": row.get("web_user_id") if row else None,
        "telegram_id": row.get("telegram_id") if row else None,
    }


async def unlink(user_id: int) -> bool:
    return await unlink_accounts(user_id)


async def mos_progress_for(user_id: int) -> dict[str, bool]:
    """MOS progress with linked peer OR-merged."""
    steps = await get_mos_progress(user_id)
    peer = await get_linked_peer(user_id)
    if not peer:
        return steps
    other = await get_mos_progress(peer)
    for key, value in other.items():
        if value:
            steps[key] = True
    return steps


async def save_mos_progress_synced(user_id: int, steps: dict[str, bool]) -> dict[str, bool]:
    await set_mos_progress(user_id, steps)
    peer = await get_linked_peer(user_id)
    if peer:
        await set_mos_progress(peer, steps)
    return steps
