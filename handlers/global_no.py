from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(F.text.lower() == "нет")
async def handle_no(msg: types.Message, state: FSMContext):
    current = await state.get_state()
    if not current:
        return

    if current.endswith("waiting_files"):
        await state.update_data(files=None)
        await msg.answer("Файлы пропущены. Продолжаем.")
        await state.clear()
        return

    if current.endswith("waiting_description"):
        await state.update_data(description="(не указано)")
        await msg.answer("Описание пропущено. Продолжаем.")
        return
