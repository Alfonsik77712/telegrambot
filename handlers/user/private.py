from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID

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


# -----------------------------
# ПОКУПКА ПРИВАТА ЗА 500₽
# -----------------------------
@router.message(F.text == "💎 500₽ навсегда")
async def buy_private_forever(msg: types.Message):

    username = msg.from_user.username or f"id{msg.from_user.id}"

    # 🔥 Уведомляем админа
    await msg.bot.send_message(
        ADMIN_ID,
        f"💎 Пользователь @{username} хочет купить приват *НАВСЕГДА* за 500₽.",
        parse_mode="Markdown"
    )

    # Кнопки для пользователя
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💳 Оплатить 500₽",
                    url="https://t.me/your_payment_link"   # сюда вставишь ссылку
                )
            ],
            [
                InlineKeyboardButton(
                    text="📤 Я оплатил",
                    callback_data="private_paid_forever"
                )
            ]
        ]
    )

    await msg.answer(
        "💎 *Приват навсегда — 500₽*\n\n"
        "После оплаты нажмите кнопку «Я оплатил» и отправьте чек.",
        reply_markup=kb,
        parse_mode="Markdown"
    )


# -----------------------------
# ПОЛЬЗОВАТЕЛЬ НАЖАЛ «Я ОПЛАТИЛ»
# -----------------------------
@router.callback_query(F.data == "private_paid_forever")
async def confirm_payment(callback: types.CallbackQuery):
    await callback.message.answer(
        "Отправьте скриншот или чек об оплате, чтобы админ подтвердил покупку."
    )


# -----------------------------
# ПОЛЬЗОВАТЕЛЬ ОТПРАВИЛ ЧЕК
# -----------------------------
@router.message(F.photo)
async def receive_payment_check(msg: types.Message):

    username = msg.from_user.username or f"id{msg.from_user.id}"

    await msg.answer("Ваш чек отправлен на проверку админу!")

    await msg.bot.send_photo(
        ADMIN_ID,
        msg.photo[-1].file_id,
        caption=(
            f"🧾 Новый чек об оплате приватки!\n"
            f"Пользователь: @{username}\n"
            f"Тип: 💎 Навсегда (500₽)"
        )
    )
