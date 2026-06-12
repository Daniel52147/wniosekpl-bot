import json
from typing import Any

from src.database import get_profile, save_profile

META_DRAFT = "__draft__"


async def save_draft(telegram_id: int, draft: dict[str, Any]) -> None:
    data = await get_profile(telegram_id) or {}
    data[META_DRAFT] = draft
    await save_profile(telegram_id, data)


async def load_draft(telegram_id: int) -> dict[str, Any] | None:
    data = await get_profile(telegram_id) or {}
    draft = data.get(META_DRAFT)
    return draft if isinstance(draft, dict) else None


async def clear_draft(telegram_id: int) -> None:
    data = await get_profile(telegram_id) or {}
    if META_DRAFT in data:
        del data[META_DRAFT]
        await save_profile(telegram_id, data)
