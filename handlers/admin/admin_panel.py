from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_ID
from utils.is_admin import is_admin
from database.db import get_db

router = Router()

def log_admin_action(admin_id: int, action: str, order_id: int | None = None):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO admin_logs (admin_id, action, order_id, created_at)
        VALUES (?, ?, ?, datetime('now'))
    """, (admin_id, action, order_id))
    db.commit()
    db.close()

@router.message(commands=["admin"])
async def admin_cmd(msg: types.Message):
    if not is_admin(msg.from_user.id):
        return await msg.answer("У вас нет доступа.")

    await msg.answer(
        "Админ-панель:\n"
        "/add_admin <id> — добавить админа\n"
        "/remove_admin <id> — удалить админа\n"
        "/admins — список админов\n"
        "/orders — все заказы"
    )

@router.message(commands=["add_admin"])
async def add_admin(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return await msg.answer("Только главный админ может назначать других.")

    parts = msg.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        return await msg.answer("Использование: /add_admin 123456789")

    new_admin = int(parts[1])

    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT OR IGNORE INTO admins (tg_id) VALUES (?)", (new_admin,))
    db.commit()
    db.close()

    log_admin_action(msg.from_user.id, f"add_admin:{new_admin}")
    await msg.answer(f"Админ {new_admin} добавлен.")

@router.message(commands=["remove_admin"])
async def remove_admin(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return await msg.answer("Только главный админ может удалять админов.")

    parts = msg.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        return await msg.answer("Использование: /remove_admin 123456789")

    admin_id = int(parts[1])

    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM admins WHERE tg_id = ?", (admin_id,))
    db.commit()
    db.close()

    log_admin_action(msg.from_user.id, f"remove_admin:{admin_id}")
    await msg.answer(f"Админ {admin_id} удалён.")

@router.message(commands=["admins"])
async def list_admins(msg: types.Message):
    if not is_admin(msg.from_user.id):
        return await msg.answer("Нет доступа.")

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT tg_id FROM admins")
    admins = cursor.fetchall()
    db.close()

    if not admins:
        return await msg.answer("Админов нет.")

    text = "Админы:\n" + "\n".join([str(a[0]) for a in admins])
    await msg.answer(text)

@router.message(commands=["orders"])
async def list_orders(msg: types.Message):
    if not is_admin(msg.from_user.id):
        return await msg.answer("Нет доступа.")

    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT id, user_id, service, description, price, status, created_at
        FROM orders
        ORDER BY created_at DESC
        LIMIT 30
    """)
    orders = cursor.fetchall()
    db.close()

    if not orders:
        return await msg.answer("Заказов пока нет.")

    for order in orders:
        order_id, user_id, service, description, price, status, created_at = order

        text = (
            f"🧾 Заказ #{order_id}\n\n"
            f"🛠 Услуга: {service}\n"
            f"💬 Описание: {description}\n"
            f"💰 Цена: {price}₽\n"
            f"👤 Пользователь: {user_id}\n"
            f"📅 Создан: {created_at}\n"
            f"📌 Статус: {status}\n"
        )

        buttons = []
        if status == "new":
            buttons = [
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
        elif status == "accepted":
            buttons = [[
                InlineKeyboardButton(
                    text="✅ Готово",
                    callback_data=f"order_done:{order_id}"
                )
            ]]

        kb = InlineKeyboardMarkup(inline_keyboard=buttons) if buttons else None
        await msg.answer(text, reply_markup=kb)

@router.callback_query(F.data.startswith("order_accept:"))
async def cb_order_accept(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("Нет доступа", show_alert=True)

    order_id = int(callback.data.split(":")[1])

    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE orders SET status = 'accepted' WHERE id = ?", (order_id,))
    db.commit()
    db.close()

    log_admin_action(callback.from_user.id, "accept", order_id)
    await callback.answer("Заказ принят")
    await callback.message.edit_reply_markup(reply_markup=None)

@router.callback_query(F.data.startswith("order_reject:"))
async def cb_order_reject(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("Нет доступа", show_alert=True)

    order_id = int(callback.data.split(":")[1])

    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE orders SET status = 'rejected' WHERE id = ?", (order_id,))
    db.commit()
    db.close()

    log_admin_action(callback.from_user.id, "reject", order_id)
    await callback.answer("Заказ отклонён")
    await callback.message.edit_reply_markup(reply_markup=None)

@router.callback_query(F.data.startswith("order_done:"))
async def cb_order_done(callback: types.CallbackQuery):
    if not is_admin(callback.from_user.id):
        return await callback.answer("Нет доступа", show_alert=True)

    order_id = int(callback.data.split(":")[1])

    db = get_db()
    cursor = db.cursor()
    cursor.execute("UPDATE orders SET status = 'done' WHERE id = ?", (order_id,))
    db.commit()
    db.close()

    log_admin_action(callback.from_user.id, "done", order_id)
    await callback.answer("Заказ завершён")
    await callback.message.edit_reply_markup(reply_markup=None)
