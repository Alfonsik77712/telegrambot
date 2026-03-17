from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
import asyncio

from config import TOKEN

from handlers.user import start, services, private, ads, support
from handlers import global_handlers

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(services.router)
    dp.include_router(private.router)
    dp.include_router(ads.router)
    dp.include_router(support.router)

    # ДОЛЖЕН БЫТЬ ПОСЛЕДНИМ
    dp.include_router(global_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
