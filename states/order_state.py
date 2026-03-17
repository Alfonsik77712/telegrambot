from aiogram.fsm.state import StatesGroup, State

class OrderState(StatesGroup):
    waiting_description = State()
    waiting_files = State()
