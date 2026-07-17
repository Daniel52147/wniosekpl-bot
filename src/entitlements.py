from src.config import AI_FREE_DAILY_LIMIT
from src.database import ai_questions_today, has_active_subscription, join_waitlist


async def user_plan(user_id: int) -> dict:
    unlimited = await has_active_subscription(user_id, "ai_subscription")
    used = await ai_questions_today(user_id)
    limit = 10_000 if unlimited else AI_FREE_DAILY_LIMIT
    left = max(limit - used, 0) if not unlimited else 10_000
    return {
        "plan": "ai_subscription" if unlimited else "free",
        "unlimited": unlimited,
        "ai_used_today": used,
        "ai_limit": limit if not unlimited else None,
        "ai_left": left if not unlimited else None,
    }


async def can_ask_ai(user_id: int) -> tuple[bool, dict]:
    plan = await user_plan(user_id)
    if plan["unlimited"]:
        return True, plan
    return (plan["ai_left"] or 0) > 0, plan


async def mark_human_review_purchased(user_id: int) -> None:
    await join_waitlist(user_id, "human_review_paid")
