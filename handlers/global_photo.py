from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from config import ADMIN_ID

router = Router()

@router.message(types.ContentType.PHOTO)
async def handle_photo(msg: types.Message, state: FSMContext):
    current = await state.get_state()

    # Если бот ждал файл для услуги
    if current and current.endswith("waiting_files"):
        await msg.answer("Файл получен! Заказ отправлен админу.")
        
        username = msg.from_user.username or f"id{msg.from_user.id}"

        await msg.bot.send_photo(
            ADMIN_ID,
            msg.photo[-1].file_id,
            caption=f"📦 Файл от @{username} для услуги"
        )

        await state.clear()
        return

    # Если это чек (приват/реклама)
    username = msg.from_user.username or f"id{msg.from_user.id}"

    await msg.answer("Ваш чек отправлен админу!")

    await msg.bot.send_photo(
        ADMIN_ID,
        msg.photo[-1].file_id,
        caption=f"🧾 Чек от @{username}"
    )
