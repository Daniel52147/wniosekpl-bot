import asyncio
import logging
import sys

from aiogram import Dispatcher
from aiogram.types import BotCommand

from src.config import BOT_TOKEN
from src.fsm_storage import SQLiteStorage
from src.telegram_session import create_bot
from src.database import init_db
from src.documents import load_all_documents
from src.form_flow import init as init_form_flow
from src.handlers import router
import src.handlers as handlers
from src.reminders import reminder_loop
from src.templates_loader import ensure_official_templates, missing_templates

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


async def main() -> None:
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не задан. Скопируйте .env.example в .env и укажите токен от @BotFather")
        sys.exit(1)

    await init_db()

    missing = missing_templates()
    if missing:
        logger.info("Downloading official templates: %s", ", ".join(missing))
        ensure_official_templates()
    handlers.DOCUMENTS = load_all_documents()
    init_form_flow(handlers.DOCUMENTS)

    bot = create_bot()
    dp = Dispatcher(storage=SQLiteStorage())
    dp.include_router(router)

    try:
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Menu główne / Main menu"),
                BotCommand(command="docs", description="Wybierz formularz"),
                BotCommand(command="lang", description="Zmień język"),
                BotCommand(command="help", description="Pomoc"),
                BotCommand(command="privacy", description="Polityka prywatności"),
                BotCommand(command="usun", description="Usuń moje dane (RODO)"),
                BotCommand(command="cancel", description="Anuluj wypełnianie"),
                BotCommand(command="ostatni", description="Powtórz ostatni formularz"),
                BotCommand(command="profil", description="Zapisane dane / Profile"),
                BotCommand(command="guide", description="Co mi potrzebne? / Guide"),
                BotCommand(command="feedback", description="Opinia / Feedback"),
            ]
        )
    except Exception as exc:
        logger.warning("set_my_commands failed: %s", exc)

    asyncio.create_task(reminder_loop(bot))
    logger.info("WniosekPL bot started (SQLite FSM + phase 4)")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
