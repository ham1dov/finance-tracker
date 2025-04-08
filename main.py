import asyncio
import logging
from config.config import token, admin_list, db_uri

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeDefault, BotCommandScopeChat
from database.manage_db import Users
from handlers.start import user_router

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)



async def main():
    bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())


    await bot.delete_webhook(drop_pending_updates=True)

    users = Users(db_uri)
    # await users.drop_table_incomes()
    # await users.drop_table_expenses()
    await users.drop_table_users()
    await users.create_table_users()
    await users.create_table_incomes()
    await users.create_table_expenses()

    for admin in admin_list:
        try:
            await bot.send_message(chat_id=admin, text="🚀 Bot is launching...")
        except Exception as e:
            logger.error(f"❌ Failed to notify admin {admin}: {e}")
    dp.include_router(user_router)


    logger.info("✅ Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("⚡ Bot stopped manually.")

    except Exception as e:
        logger.critical(f"🚨 Unexpected error: {e}", exc_info=True)