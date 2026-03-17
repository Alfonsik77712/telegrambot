from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import main_menu

router = Router()

@router.message(F.text == "⬅️ Назад")
async def go_back(msg: types.Message, state: FSMContext):
    await state.clear()
    await msg.answer("Главное меню:", reply_markup=main_menu)
