from aiogram.fsm.state import State, StatesGroup


class FormStates(StatesGroup):
    waiting_answer = State()
    confirming = State()
    package_collecting = State()
    package_confirming = State()
    waiting_podstawa_custom = State()
    profile_editing = State()
    waiting_feedback = State()
