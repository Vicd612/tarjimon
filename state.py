from aiogram.fsm.state import State, StatesGroup

class AddLang(StatesGroup):
    name = State()
    code = State()