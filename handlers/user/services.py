from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from states.order_state import OrderState
from database.db import get_db
from config import ADMIN_ID

router = Router()

services_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🛠 Сборка — 250₽")],
        [KeyboardButton(text="🎨 Худ — 150₽")],
        [KeyboardButton(text="🖼 Фикс PNG — 100₽")],
        [KeyboardButton(text="📸 Оформление — 100₽")],
        [KeyboardButton(text="⬅️ Назад")]
    ],
    resize_keyboard=True
)

@router.message(lambda m: m.text == "📦 Услуги")
async def open_services(msg: types.Message):
    await msg.answer("Выберите услугу:", reply_markup=services_menu)

@router.message(lambda m: "₽" in m.text and "⬅️" not in m.text)
async def choose_service(msg: types.Message, state: FSMContext):
    service_full = msg.text
    try:
        name_part, price_part = service_full.split("—")
        service_name = name_part.strip()
        price = int(price_part.replace("₽", "").strip())
    except Exception:
        return await msg.answer("Не удалось распознать услугу, попробуйте ещё раз.")

    await state.update_data(service=service_name, price=price)
    await msg.answer("Опишите заказ:")
    await state.set_state(OrderState.waiting_description)

@router.message(OrderState.waiting_description)
async def get_description(msg: types.Message, state: FSMContext):
    await state.update_data(description=msg.text)
    await msg.answer("Прикрепите файлы (если есть) или напишите 'нет'")
    await state.set_state(OrderState.waiting_files)

@router.message(OrderState.waiting_files)
async def finish_order(msg: types.Message, state: FSMContext):
    data = await state.get_data()

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO orders (user_id, service, description, price, status, created_at)
        VALUES (?, ?, ?, ?, ?, datetime('now'))
    """, (
        msg.from_user.id,
        data["service"],
        data["description"],
        data["price"],
        "new"
    ))

    order_id = cursor.lastrowid
    db.commit()
    db.close()

    await msg.answer("Ваш заказ отправлен админу!")
    await state.clear()

    text = (
        f"🆕 Новый заказ #{order_id}\n\n"
        f"🛠 Услуга: {data['service']}\n"
        f"💬 Описание: {data['description']}\n"
        f"💰 Цена: {data['price']}₽\n"
        f"👤 Пользователь: {msg.from_user.id}\n"
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Принять",
                    callback_data=f"order_accept:{order_id}"
                ),
                InlineKeyboardButton(
                    text="❌ Отклонить",
                    callback_data=f"order_reject:{order_id}"
                )
            ]
        ]
    )

    await msg.bot.send_message(ADMIN_ID, text, reply_markup=kb)
