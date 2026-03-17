from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID

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


# -----------------------------
# ОБРАБОТКА ЛЮБОГО ВАРИАНТА РЕКЛАМЫ
# -----------------------------
@router.message(F.text.regexp(r".+—\s*\d+₽"))
async def buy_ad(msg: types.Message):

    username = msg.from_user.username or f"id{msg.from_user.id}"
    ad_type = msg.text

    # 🔥 Уведомляем админа
    await msg.bot.send_message(
        ADMIN_ID,
        f"📢 Пользователь @{username} хочет купить рекламу:\n\n{ad_type}"
    )

    # Кнопки для пользователя
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"💳 Оплатить ({ad_type.split('—')[1].strip()})",
                    url="https://t.me/your_payment_link"   # сюда вставишь ссылку
                )
            ],
            [
                InlineKeyboardButton(
                    text="📤 Я оплатил",
                    callback_data=f"ad_paid:{ad_type}"
                )
            ]
        ]
    )

    await msg.answer(
        f"📢 *Реклама: {ad_type}*\n\n"
        "После оплаты нажмите «Я оплатил» и отправьте чек.",
        reply_markup=kb,
        parse_mode="Markdown"
    )


# -----------------------------
# ПОЛЬЗОВАТЕЛЬ НАЖАЛ «Я ОПЛАТИЛ»
# -----------------------------
@router.callback_query(F.data.startswith("ad_paid:"))
async def confirm_ad_payment(callback: types.CallbackQuery):
    await callback.message.answer(
        "Отправьте скриншот или чек об оплате, чтобы админ подтвердил покупку."
    )


# -----------------------------
# ПОЛЬЗОВАТЕЛЬ ОТПРАВИЛ ЧЕК
# -----------------------------
@router.message(F.photo)
async def receive_ad_check(msg: types.Message):

    username = msg.from_user.username or f"id{msg.from_user.id}"

    await msg.answer("Ваш чек отправлен на проверку админу!")

    await msg.bot.send_photo(
        ADMIN_ID,
        msg.photo[-1].file_id,
        caption=(
            f"🧾 Новый чек об оплате рекламы!\n"
            f"Пользователь: @{username}"
        )
    )
