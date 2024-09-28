from create_bot import dp, bot, db, check_sub_channels
from db import Database
from aiogram import types, Dispatcher
# from states import FSMWelcome
# from aiogram.dispatcher import FSMContext
# from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards import welcome_btn as btn
# from keyboards import client_btn as nav
from keyboards import check_subscribe_btn as sub
from keyboards import contest as cont
import config as con
import datetime
from urllib.parse import urlparse
from aiogram.types.web_app_info import WebAppInfo


# # @dp.message_handler(commands=['start'], state=None)
# async def start(message: types.Message):
#     if message.chat.type == 'private':
#         user_id = message.from_user.id

#         if not db.user_exists(user_id):
#             if await check_sub_channels(con.CHANNELS, user_id):
#                 start_command = message.text
#                 referrer_id = str(start_command[7:])

#                 try:
#                     if referrer_id:
#                         # # if referrer_id.isdigit() and int(referrer_id) != user_id:
#                         # #     db.add_user(user_id, referrer_id)
#                         # #     referrals = int(db.get_number_of_referrals(referrer_id)) + 1
#                         # #     db.set_number_of_referrals(referrer_id, referrals)

#                         #     # scores = int(db.get_scores(referrer_id)) + 50
#                         #     # db.set_scores(referrer_id, scores)

#                         #     # db.null_like_dislike(user_id)
#                         #     # db.null_messages(user_id)
#                         #     # db.null_scores(user_id)
#                         #     # db.null_number_of_referrals(user_id)
#                         #     # db.set_data(user_id, datetime.datetime.now())

#                         #     # await FSMWelcome.name.set()
#                         #     # await message.answer(" Привет, я Анонимный ЧатБот!")

#                         #     await bot.send_message(message.from_user.id, 'Chouse language:', reply_markup=btn.langMenu)
#                         #     # await bot.send_message(user_id, 'Заполнение анкетки:')
#                         #     # await message.reply('Как я могу обращаться к тебе?🤔')

#                         # else:
#                         #     # Обработка текстового реферрала
#                         #     # referrer_id = referrer_id.lower()
#                         #     # if not db.user_exists(referrer_id):
#                         #     #     db.add_referral(referrer_id)

#                         #     # db.add_user(user_id, referrer_id)
#                         #     # referrals = int(db.get_number_of_referrals_ref(referrer_id)) + 1
#                         #     # db.set_number_of_referrals_ref(referrer_id, referrals)

#                         #     # db.null_like_dislike(user_id)
#                         #     # db.null_messages(user_id)
#                         #     # db.null_scores(user_id)
#                         #     # db.null_number_of_referrals(user_id)
#                         #     # db.set_data(user_id, datetime.datetime.now())

#                         #     # await FSMWelcome.name.set()
#                         #     # await message.answer(" Привет, я Анонимный ЧатБот!")
#                         #     await bot.send_message(message.from_user.id, 'Chouse language:', reply_markup=btn.langMenu)                         
#                         #     # await bot.send_message(user_id, 'Заполнение анкетки:')
#                         #     # await message.reply('Как я могу обращаться к тебе?🤔')
#                         # await bot.send_message(message.from_user.id, 'Chouse language:', reply_markup=btn.langMenu)
#                         import eel
#                         @eel.expose
#                         def take_py(txt_in):
#                             global txt
#                             txt = txt_in
#                         await bot.send_message(message.from_user.id, txt, reply_markup=btn.openwebapp)   
#                     else:
#                         # Обработка отсутствия реферрала
#                         # db.add_user(user_id)
#                         # db.null_like_dislike(user_id)
#                         # db.null_messages(user_id)
#                         # db.null_scores(user_id)
#                         # db.null_number_of_referrals(user_id)
#                         # db.set_data(user_id, datetime.datetime.now())

#                         # await FSMWelcome.name.set()
#                         # await message.answer(" Привет, я Анонимный ЧатБот!")
#                         # await bot.send_message(message.from_user.id, 'Chouse language:', reply_markup=btn.langMenu)
#                         import eel
#                         @eel.expose
#                         def take_py(txt_in):
#                             global txt
#                             txt = txt_in
#                         await bot.send_message(message.from_user.id, txt, reply_markup=btn.openwebapp)                         


#                 except ValueError as e:
#                     print(f"Error: {e}")
#                     await message.reply("Произошла ошибка при обработке реферрала.")


#                 # await message.reply("")
#             else:
#                 await bot.send_message(user_id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

#         else:
#             if not db.get_block(user_id):
#                 # await bot.send_message(message.from_user.id, 'Chouse language:', reply_markup=btn.langMenu)
#                 await bot.send_message(message.from_user.id, 'Hi', reply_markup=btn.openwebapp)                             

#             else:
#                 await bot.send_message(user_id, "Вы заблокированы!")

#     else:
#         await bot.send_message(user_id, 'Бот работает только в приватных чатах!')


# # @dp.message_handler(commands=['start'], state=None) 
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Hi', reply_markup=btn.openwebapp) 
#----------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(text='edit_questionnaire')
async def get_account_photo(message: types.Message):
    if db.get_block(message.from_user.id) == 0:
        if await check_sub_channels(con.CHANNELS, message.from_user.id):
            foto = await message.from_user.get_profile_photos()
            # foto = a.photos[0][1].file_id
            await bot.send_photo(message.from_user.id, photo = foto)
            # from json import dumps

            # bot.execute_script("document.getElementById('avatar').value+=" +
            #                       dumps(foto))
        else:
            await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())
    else:
        await bot.send_message(message.from_user.id, "Вы заблокированы!")

# #----------------------------------------------------------------------------------------------------------------
# #----------------------------------------------------------------------------------------------------------------

# # @dp.message_handler(state=FSMWelcome.name)
# async def load_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         if await check_sub_channels(con.CHANNELS, message.from_user.id):
#             max_length = 50  # Максимальное количество символов
#             text = message.text
#             if len(text) > max_length:
#                 await bot.send_photo(message.from_user.id, caption = 'Ваше сообщение было отформатировано, так как превышает разрешённые 50 символов. Вы всегда можете изменить свою анкету!', photo = open('Images/404.png', 'rb'))
#                 text = text[:max_length]
#                 data['name'] = text
#                 # await message.reply("Ваше сообщение было отформатировано, так как превышает максимальное количество символов.")
#             else:
#                 data['name'] = text
#             db.set_name(message.from_user.id, text)
#             await message.answer('Сколько тебе лет?🔞')
#             await FSMWelcome.next()
#         else:
#             await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

# #----------------------------------------------------------------------------------------------------------------

# # @dp.message_handler(state=FSMWelcome.age)
# async def load_age(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         if await check_sub_channels(con.CHANNELS, message.from_user.id):
#             age = (message.text) if message.text.isdigit() else None
#             if age is not None:
#                 if int(age) < 0 or int(age) > 120:
#                     await bot.send_photo(message.from_user.id, caption = "Был указан некорректный возраст. Установлен возраст '0'.", photo = open('Images/404.png', 'rb'))
#                     age = "0"
#                     data['age'] = age
#                     # await message.reply("Был указан некорректный возраст. Установлен возраст '0'.")
#                 elif len(age) > 3:
#                     await bot.send_photo(message.from_user.id, caption = "Был указан некорректный возраст. Установлен возраст '0'.", photo = open('Images/404.png', 'rb'))
#                     age = "0"
#                     data['age'] = age
#                 else:
#                     data['age'] = age

#             db.set_age(message.from_user.id, age)
#             await message.answer('💬 Расскажи немного о себе, кого ты ищешь, чем увлекаешься и т.д.')
#             await FSMWelcome.next()

#         else:
#             await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

# #----------------------------------------------------------------------------------------------------------------

# # @dp.message_handler(state=FSMWelcome.text)
# async def load_text(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         if await check_sub_channels(con.CHANNELS, message.from_user.id):
#             max_length = 500  # Максимальное количество символов
#             text = message.text
#             if len(text) > max_length:
#                 await bot.send_photo(message.from_user.id, caption = 'Ваше сообщение было отформатировано, так как превышает разрешённые 500 символов. Вы всегда можете изменить свою анкету!', photo = open('Images/404.png', 'rb'))
#                 text = text[:max_length]
#                 data['text'] = text
#                 # await message.reply("Ваше сообщение было отформатировано, так как превышает максимальное количество символов.")
#             else:
#                 data['text'] = text
#             db.set_text(message.from_user.id, text)
#             await message.answer('🚻 Укажи свой пол:', reply_markup=btn.walcome_markup)
#             await FSMWelcome.next()
#         else:
#             await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())


# #----------------------------------------------------------------------------------------------------------------

# # @dp.callback_query_handler(text='man', state=FSMWelcome.gender)
# async def load_gender_man(callback_query: types.CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         if await check_sub_channels(con.CHANNELS, callback_query.from_user.id):
#             # data['gender'] = message.text
#             data['gender'] = '👨Парень'
#             db.set_gender(callback_query.from_user.id, data['gender'])
#             await bot.send_message(callback_query.from_user.id, 'Анкета заполнена, удачного общения!')
#             await bot.send_message(callback_query.from_user.id, """📜 Правила чата. Прочти перед использованием:
# 1. Уважайте других участников✊
# 2. Сохраняйте анонимность🎭
# 3. Не публикуйте незаконный контент🔞
# 4. Избегайте спама и рекламы📢

# 📝 Помните, что администрация бота имеет право изменять правила по своему усмотрению для обеспечения комфортного опыта для всех участников.""", reply_markup=nav.find_partner)
#             await state.finish()
#         else:
#             await bot.send_message(callback_query.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

# # @dp.callback_query_handler(text='woman', state=FSMWelcome.gender)
# async def load_gender_woman(callback_query: types.CallbackQuery, state: FSMContext):
#     async with state.proxy() as data:
#         if await check_sub_channels(con.CHANNELS, callback_query.from_user.id):
#             data['gender'] = '👩Девушка'
#             db.set_gender(callback_query.from_user.id, data['gender'])
#             await bot.send_message(callback_query.from_user.id, 'Анкета заполнена, удачного общения!')
#             await bot.send_message(callback_query.from_user.id, """📜 Правила чата. Прочти перед использованием:
# 1. Уважайте других участников✊
# 2. Сохраняйте анонимность🎭
# 3. Не публикуйте незаконный контент🔞
# 4. Избегайте спама и рекламы📢

# 📝 Помните, что администрация бота имеет право изменять правила по своему усмотрению для обеспечения комфортного опыта для всех участников.""", reply_markup=nav.find_partner)
#             await state.finish()
#         else:
#             await bot.send_message(callback_query.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

# #----------------------------------------------------------------------------------------------------------------

#Регистрируем хендлеры
def register_handlers_welcome(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(get_account_photo, commands=['photo'])
    # dp.register_callback_query_handler(edit_questionnaire, text='edit_questionnaire')
    # dp.register_message_handler(load_name, state=FSMWelcome.name)
    # dp.register_message_handler(load_age, state=FSMWelcome.age)
    # dp.register_message_handler(load_text, state=FSMWelcome.text)
    # dp.register_callback_query_handler(load_gender_man, text='man', state=FSMWelcome.gender)
    # dp.register_callback_query_handler(load_gender_woman, text='woman', state=FSMWelcome.gender)
