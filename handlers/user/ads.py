from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

ads_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⏱ 24 часа — 100₽")],
        [KeyboardButton(text="📆 Неделя — 500₽")],
        [KeyboardButton(text="🗓 Месяц — 1500₽")],
        [KeyboardButton(text="📌 Закреп +50₽")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

@router.message(F.text == "📢 Реклама")
async def open_ads(msg: types.Message):
    await msg.answer("Выберите формат рекламы:", reply_markup=ads_menu)
