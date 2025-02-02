from create_bot import dp, bot, db, check_sub_channels
from keyboards import claim_btn as nav
from keyboards import client_btn as navs
from states import FCMClaim
import config as con
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from aiogram.utils.markdown import quote_html

# @dp.message_handler(ISPrivate(), lambda message: message.text == "Жалоба ⚠️")
async def claim(message: types.Message):
    if(not db.get_block(message.from_user.id)):
        if await check_sub_channels(con.CHANNELS, message.from_user.id):

            chat = db.get_chat(message.from_user.id)

            # await message.answer("""Введите причину жалобы или выберите из перечисленного!""", reply_markup=nav.claim)
            await bot.send_photo(message.from_user.id, caption = 'Введите причину жалобы или выберите из перечисленного!', photo = open('Images/report.png', 'rb'), reply_markup=nav.claim)


            await FCMClaim.text.set()
        else:
            await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

    else:
        await bot.send_message(message.from_user.id, "Вы заблокированы!")

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(ISPrivate(), state=FCMClaim.text)
async def claim_text(message: types.Message, state: FSMContext):
    if await check_sub_channels(con.CHANNELS, message.from_user.id):
        
        answer = message.text
        await state.update_data(text=answer)
        await message.answer(text=answer, reply_markup=nav.markup)
        await FCMClaim.state.set()

    else:
        await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())
#----------------------------------------------------------------------------------------------------------------

# @dp.calback_query_handler(text='next', state=FCMClaim.state)
async def start(call: types.CallbackQuery, state: FSMContext):
    if await check_sub_channels(con.CHANNELS, call.from_user.id):
        chat = db.get_chat(call.from_user.id)

        id = chat[1]
        idname = await bot.get_chat(id)
        named = quote_html(idname.username)

        users = db.get_users()
        data = await state.get_data()
        text = data.get('text')
        await state.finish()

        await bot.send_message(-1001949092880, text=text)
        await bot.send_message(-1001949092880, f"""ЖАЛОБА!!!!!!👆
\nОт: {call.from_user.mention}
user_id: {call.from_user.id}
full_name: {call.from_user.full_name}👆


На:
id: {chat[1]}
username: @{named}""")

        await call.message.answer('Жалоба отправлена', reply_markup=navs.disconnected)

    else:
        await bot.send_message(call.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())
#----------------------------------------------------------------------------------------------------------------

# @dp.calback_query_handler(text='add_photo', state=FCMClaim.state)
async def add_photo(call: types.CallbackQuery):
    if await check_sub_channels(con.CHANNELS, call.from_user.id):
        await call.message.answer('Пришлите фото')
        await FCMClaim.photo.set()
    else:
        await bot.send_message(call.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(ISPrivate(), state=FCMClaim.photo, content_types=types.ContentType.PHOTO)
async def claim_photo(message: types.Message, state: FSMContext):
    if await check_sub_channels(con.CHANNELS, message.from_user.id):

        photo_file_id = message.photo[-1].file_id
        await state.update_data(photo=photo_file_id)
        data = await state.get_data()
        text = data.get('text')
        photo = data.get('photo')
        markup = InlineKeyboardMarkup(row_width=2,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text='Далее', callback_data='next'),
                                                InlineKeyboardButton(text='Отменить', callback_data='quit')
                                            ]
                                        ])
        await message.answer_photo(photo=photo, caption=text, reply_markup=markup)

    else:
        await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

#----------------------------------------------------------------------------------------------------------------

# @dp.calback_query_handler(text='next', state=FCMClaim.photo)
async def start_p(call: types.CallbackQuery, state: FSMContext):
    if await check_sub_channels(con.CHANNELS, call.from_user.id):

        chat = db.get_chat(call.from_user.id)

        id = chat[1]
        idname = await bot.get_chat(id)
        named = quote_html(idname.username)

        users = db.get_users()
        data = await state.get_data()
        text = data.get('text')
        photo = data.get('photo')
        await state.finish()

        await bot.send_photo(-1001949092880, photo=photo, caption=text)
        await bot.send_message(-1001949092880, f"""ЖАЛОБА!!!!!!👆
\nОт: {call.from_user.mention}
user_id: {call.from_user.id}
full_name: {call.from_user.full_name}👆


На:
id: {chat[1]}
username: @{named}""")

        await call.message.answer('Жалоба отправлена', reply_markup=navs.disconnected)
    else:
        await bot.send_message(call.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(ISPrivate(), state=FCMClaim.photo)
async def no_photo(message: types.Message):
    if await check_sub_channels(con.CHANNELS, message.from_user.id):

        markup = InlineKeyboardMarkup(row_width=2,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text='Отменить', callback_data='quit')
                                            ]
                                        ])
        await message.answer('Пришлите фото', reply_markup=markup)

    else:
        await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

# @dp.calback_query_handler(text='quit', state=[FCMAiling.text, FCMAiling.photo, FCMAiling.state])
async def quit(call: types.CallbackQuery, state: FSMContext):
    if await check_sub_channels(con.CHANNELS, call.from_user.id):

        await state.finish()
        await bot.send_message(call.from_user.id, 'Жалоба отменена', reply_markup=navs.disconnected)
  
    else:
        await bot.send_message(call.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())
#----------------------------------------------------------------------------------------------------------------

#Регистрируем хендлеры
def register_handlers_claim(dp: Dispatcher):
    dp.register_message_handler(claim, lambda message: message.text == "Жалоба ⚠️")
    dp.register_message_handler(claim_text, state=FCMClaim.text)
    dp.register_callback_query_handler(start, text='next', state=FCMClaim.state)
    dp.register_callback_query_handler(add_photo, text='add_photo', state=FCMClaim.state)
    dp.register_message_handler(claim_photo,state=FCMClaim.photo, content_types=types.ContentType.PHOTO)
    dp.register_callback_query_handler(start_p, text='next', state=FCMClaim.photo)
    dp.register_message_handler(no_photo, state=FCMClaim.photo)
    dp.register_callback_query_handler(quit, text='quit', state=[FCMClaim.text, FCMClaim.photo, FCMClaim.state])