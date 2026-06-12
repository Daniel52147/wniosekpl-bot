import logging
import ssl

import certifi
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from src.config import BOT_TOKEN, RELAX_SSL

logger = logging.getLogger(__name__)


def create_bot() -> Bot:
    session = AiohttpSession()
    if RELAX_SSL:
        session._connector_init["ssl"] = ssl._create_unverified_context()
        logger.warning("RELAX_SSL=true — SSL verification disabled (local dev only)")
    else:
        session._connector_init["ssl"] = ssl.create_default_context(cafile=certifi.where())

    return Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
