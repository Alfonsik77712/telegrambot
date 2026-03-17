from aiogram import Router, types

router = Router()

@router.message(lambda m: m.text == "💬 Поддержка")
async def support(msg: types.Message):
    await msg.answer("Поддержка: @your_support_username")
