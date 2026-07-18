"""Link web account ↔ Telegram so MOS progress and drafts stay one."""

from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone

from src.config import BOT_USERNAME
from src.database import (
    add_calendar_event,
    claim_link_code,
    create_link_code,
    get_link_status,
    get_linked_peer,
    get_mos_progress,
    get_subscription,
    list_calendar_events,
    set_mos_progress,
    unlink_accounts,
    update_subscription_record,
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


async def _merge_calendar(a: int, b: int) -> int:
    """Copy missing open calendar events both ways. Returns copied count."""
    copied = 0
    for src, dst in ((a, b), (b, a)):
        src_events = await list_calendar_events(src)
        dst_events = await list_calendar_events(dst)
        seen = {(e.get("title"), e.get("due_at"), e.get("kind")) for e in dst_events}
        for event in src_events:
            key = (event.get("title"), event.get("due_at"), event.get("kind"))
            if key in seen:
                continue
            await add_calendar_event(
                dst,
                title=event.get("title") or "MOS",
                due_at=event.get("due_at") or "",
                kind=event.get("kind") or "custom",
                notes=event.get("notes") or "",
            )
            seen.add(key)
            copied += 1
    return copied


async def _merge_subscriptions(a: int, b: int) -> bool:
    """Copy the better active subscription onto the peer without one."""
    sa = await get_subscription(a)
    sb = await get_subscription(b)

    def score(sub: dict | None) -> tuple:
        if not sub or sub.get("status") != "active":
            return (0, "")
        return (1, sub.get("expires_at") or "")

    best = sa if score(sa) >= score(sb) else sb
    if not best or best.get("status") != "active":
        return False
    for uid in (a, b):
        cur = await get_subscription(uid)
        if cur and cur.get("status") == "active" and (cur.get("expires_at") or "") >= (
            best.get("expires_at") or ""
        ):
            continue
        await update_subscription_record(
            uid,
            plan=best.get("plan") or "ai_subscription",
            status=best.get("status") or "active",
            source=best.get("source") or "link_sync",
            expires_at=best.get("expires_at"),
            stripe_subscription_id=best.get("stripe_subscription_id"),
            cancel_at_period_end=bool(best.get("cancel_at_period_end")),
        )
    return True


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
    calendar_copied = await _merge_calendar(web_user_id, telegram_id)
    sub_synced = await _merge_subscriptions(web_user_id, telegram_id)
    return {
        "ok": True,
        "web_user_id": web_user_id,
        "telegram_id": telegram_id,
        "steps": steps,
        "calendar_copied": calendar_copied,
        "subscription_synced": sub_synced,
        "synced": ["mos_progress", "web_drafts", "calendar", "subscription"],
    }


async def status_for(user_id: int) -> dict:
    row = await get_link_status(user_id)
    peer = await get_linked_peer(user_id)
    return {
        "linked": peer is not None,
        "peer_id": peer,
        "web_user_id": row.get("web_user_id") if row else None,
        "telegram_id": row.get("telegram_id") if row else None,
        "syncs": ["mos_progress", "web_drafts", "calendar", "subscription"],
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
