from aiogram import Router, types, F

router = Router()

@router.message(F.text == "💬 Поддержка")
async def support(msg: types.Message):
    await msg.answer("Поддержка: @your_support_username")

@router.message(F.text == "ℹ️ О нас")
async def about(msg: types.Message):
    await msg.answer("Мы — сервис, который выполняет услуги быстро и качественно!")
