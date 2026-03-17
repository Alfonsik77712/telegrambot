from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📦 Услуги")],
        [KeyboardButton(text="🔐 Приват"), KeyboardButton(text="📢 Реклама")],
        [KeyboardButton(text="💬 Поддержка"), KeyboardButton(text="ℹ️ О нас")]
    ],
    resize_keyboard=True
)
