from aiogram import Router, types, F

router = Router()

@router.message(F.text == "💬 Поддержка")
async def support(msg: types.Message):
    await msg.answer("Поддержка: @your_support_username")
