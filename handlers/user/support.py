from aiogram import Router, types, F
from keyboards.main_menu import main_menu

router = Router()

@router.message(F.text == "💬 Поддержка")
async def support(msg: types.Message):
    await msg.answer("Поддержка: @your_support_username")

@router.message(F.text == "⬅️ Назад")
async def go_back(msg: types.Message):
    await msg.answer("Главное меню:", reply_markup=main_menu)
