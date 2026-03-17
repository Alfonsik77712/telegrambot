from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
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

@router.message(F.text == "📦 Услуги")
async def open_services(msg: types.Message):
    await msg.answer("Выберите услугу:", reply_markup=services_menu)

@router.message(F.text.regexp(r".+—\s*\d+₽"))
async def choose_service(msg: types.Message, state: FSMContext):
    service_full = msg.text
    name_part, price_part = service_full.split("—")
    service_name = name_part.strip()
    price = int(price_part.replace("₽", "").strip())

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
        INSERT INTO orders (user_id, username, service, description, price, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'))
    """, (
        msg.from_user.id,
        msg.from_user.username or f"id{msg.from_user.id}",
        data["service"],
        data["description"],
        data["price"],
        "new"
    ))

    order_id = cursor.lastrowid
    db.commit()
    db.close()

    username = msg.from_user.username or f"id{msg.from_user.id}"

    text = (
        f"🆕 Новый заказ #{order_id}\n\n"
        f"🛠 Услуга: {data['service']}\n"
        f"💬 Описание: {data['description']}\n"
        f"💰 Цена: {data['price']}₽\n"
        f"👤 Пользователь: @{username}\n"
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Принять", callback_data=f"order_accept:{order_id}"),
                InlineKeyboardButton(text="❌ Отклонить", callback_data=f"order_reject:{order_id}")
            ]
        ]
    )

    await msg.answer("Ваш заказ отправлен админу!")
    await state.clear()
    await msg.bot.send_message(ADMIN_ID, text, reply_markup=kb)
