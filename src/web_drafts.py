"""Persist web PDF form field answers per user + document."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.database import get_profile, save_profile

META_WEB_DRAFTS = "__web_drafts__"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


async def get_doc_draft(user_id: int, doc_id: str) -> dict[str, Any] | None:
    data = await get_profile(user_id) or {}
    drafts = data.get(META_WEB_DRAFTS) or {}
    if not isinstance(drafts, dict):
        return None
    draft = drafts.get(doc_id)
    return draft if isinstance(draft, dict) else None


async def save_doc_draft(
    user_id: int,
    doc_id: str,
    answers: dict[str, Any],
) -> dict[str, Any]:
    data = await get_profile(user_id) or {}
    drafts = data.get(META_WEB_DRAFTS)
    if not isinstance(drafts, dict):
        drafts = {}
    payload = {
        "answers": {str(k): ("" if v is None else str(v)) for k, v in (answers or {}).items()},
        "updated_at": _now(),
    }
    drafts[doc_id] = payload
    data[META_WEB_DRAFTS] = drafts
    await save_profile(user_id, data)
    return payload


async def clear_doc_draft(user_id: int, doc_id: str) -> None:
    data = await get_profile(user_id) or {}
    drafts = data.get(META_WEB_DRAFTS)
    if not isinstance(drafts, dict) or doc_id not in drafts:
        return
    del drafts[doc_id]
    data[META_WEB_DRAFTS] = drafts
    await save_profile(user_id, data)


async def merge_web_drafts(from_user: int, to_user: int) -> None:
    """Copy missing drafts from one profile onto another (link sync)."""
    src = await get_profile(from_user) or {}
    dst = await get_profile(to_user) or {}
    src_drafts = src.get(META_WEB_DRAFTS) if isinstance(src.get(META_WEB_DRAFTS), dict) else {}
    dst_drafts = dst.get(META_WEB_DRAFTS) if isinstance(dst.get(META_WEB_DRAFTS), dict) else {}
    if not src_drafts:
        return
    changed = False
    for doc_id, draft in src_drafts.items():
        if doc_id not in dst_drafts and isinstance(draft, dict):
            dst_drafts[doc_id] = draft
            changed = True
    if changed:
        dst[META_WEB_DRAFTS] = dst_drafts
        await save_profile(to_user, dst)
