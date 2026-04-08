"""
Entry point for the Talking Head Telegram bot.
"""
import asyncio
import logging

from core.loader import bot, dp
import handler.include_router  # noqa: F401


async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
