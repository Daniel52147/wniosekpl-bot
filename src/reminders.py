import asyncio
import logging
from datetime import datetime, timedelta, timezone

from aiogram import Bot

from src.database import fetch_due_reminders, mark_reminder_sent

logger = logging.getLogger(__name__)

REMINDER_TEXT = {
    "ru": (
        "🔔 <b>WniosekPL</b>\n"
        "Напоминание: проверьте meldunek / продление pobytu.\n"
        "Нужен новый PDF? /docs"
    ),
    "en": "🔔 Reminder: check your meldunek / residence status. /docs",
    "ua": "🔔 Нагадування: перевірте meldunek. /docs",
    "pl": "🔔 Przypomnienie: sprawdź meldunek / status pobytu. /docs",
}


async def reminder_loop(bot: Bot, interval_sec: int = 3600) -> None:
    while True:
        try:
            due = await fetch_due_reminders()
            for row in due:
                rid, telegram_id, lang = row["id"], row["telegram_id"], row.get("lang") or "ru"
                text = REMINDER_TEXT.get(lang, REMINDER_TEXT["ru"])
                try:
                    await bot.send_message(telegram_id, text)
                    await mark_reminder_sent(rid)
                except Exception as exc:
                    logger.warning("Reminder %s failed: %s", rid, exc)
        except Exception as exc:
            logger.error("Reminder loop error: %s", exc)
        await asyncio.sleep(interval_sec)


def default_remind_at(days: int = 25) -> str:
    dt = datetime.now(timezone.utc) + timedelta(days=days)
    return dt.isoformat()
