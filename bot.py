import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import TOKEN

from handlers.user import start, services, private, ads, support
from handlers.admin import admin_panel

async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.include_router(start.router)
    dp.include_router(services.router)
    dp.include_router(private.router)
    dp.include_router(ads.router)
    dp.include_router(support.router)

    dp.include_router(admin_panel.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
