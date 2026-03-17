from aiogram import Router, types
from aiogram.filters import Command
from keyboards.main_menu import main_menu
from database.db import init_db

router = Router()

@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    init_db()
    await msg.answer(
        "Привет! Я бот сервиса. Выберите действие:",
        reply_markup=main_menu
    )
