from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

private_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⭐ 300 звёзд / месяц")],
        [KeyboardButton(text="💎 500₽ навсегда")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

@router.message(F.text == "🔐 Приват")
async def open_private(msg: types.Message):
    await msg.answer("Выберите вариант:", reply_markup=private_menu)
