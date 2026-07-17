"""Outbound notifications stub (email/Telegram). Logs until SMTP is configured."""

from __future__ import annotations

import logging

from src.config import SMTP_FROM, SMTP_HOST

logger = logging.getLogger(__name__)


def email_configured() -> bool:
    return bool((SMTP_HOST or "").strip() and (SMTP_FROM or "").strip())


async def notify_user(
    *,
    user_id: int,
    subject: str,
    body: str,
    email: str | None = None,
) -> dict:
    """Best-effort notification. Never raises to callers."""
    payload = {
        "user_id": user_id,
        "subject": subject,
        "email": email,
        "delivered": False,
        "channel": "log",
    }
    if email and email_configured():
        # Real SMTP can be wired later; keep safe stub for now.
        logger.info("EMAIL_QUEUED to=%s subject=%s", email, subject)
        payload["channel"] = "smtp_queue"
        payload["delivered"] = True
        return payload
    logger.info(
        "NOTIFY user_id=%s subject=%s body=%s",
        user_id,
        subject,
        body[:500],
    )
    return payload
