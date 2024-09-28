from aiogram.dispatcher.filters.state import State, StatesGroup

class FCMPromo(StatesGroup):
	code = State()