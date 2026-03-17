from aiogram import Router, types
from aiogram.filters import Text

router = Router()

@router.message(Text("💬 Поддержка"))
async def support(msg: types.Message):
    await msg.answer("Поддержка: @your_support_username")
