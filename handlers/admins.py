
from create_bot import dp, bot, db, check_sub_channels
import config as con
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import quote_html
from aiogram.dispatcher.filters.state import State, StatesGroup

class FCMInfo(StatesGroup):
	id = State()

# @dp.message_handler(text='/get_info', chat_id=con.admins)
async def get_info(message: types.Message):
	await message.answer(f'Введите id:')
	await FCMInfo.id.set()


# @dp.message_handler(ISPrivate(), state=FCMAiling.id, chat_id=con.admins)
async def get_id(message: types.Message, state: FSMContext):
	id = message.text
	idname = await bot.get_chat(id)
	named = quote_html(idname.username)
	await bot.send_message(message.from_user.id, f"""
id: {id}
username: @{named}
data: {db.get_data(id)}
\n
АНКЕТА: \n
{con.questionnaire(id)}
""")
	await state.finish()

#Регистрируем хендлеры
def register_handlers_admins(dp: Dispatcher):
    dp.register_message_handler(get_info, text='/get_info', chat_id=con.admins)
    dp.register_message_handler(get_id, state=FCMInfo.id, chat_id=con.admins)
