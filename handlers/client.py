from create_bot import dp, bot, db, check_sub_channels
from keyboards import client_btn as nav
from keyboards import menu_btn as navs
from keyboards import check_subscribe_btn as sub
from keyboards import rate_btn as rate
import config as con
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
import aiogram

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(lambda message: message.text == "Искаль партнёра 🔍")
async def find__partner(message: types.Message):
    if message.chat.type == 'private':
        if(not db.get_block(message.from_user.id)):
            if await check_sub_channels(con.CHANNELS, message.from_user.id):

                partner = db.get_queue()

                if db.create_chat(message.from_user.id, partner) is False:
                    db.add_queue(message.from_user.id)

                    await message.answer("Поиск партнёра...", reply_markup=nav.stop_searching)

                else:
                    num_chats_p = db.get_num_chats(partner)
                    num_chats_p += 1
                    db.set_num_chats(partner, num_chats_p)
                    num_chats = db.get_num_chats(message.from_user.id)
                    num_chats += 1
                    db.set_num_chats(message.from_user.id, num_chats)

                    db.delete_queue(message.from_user.id)
                    db.delete_queue(partner)

                    await message.answer("Вы подключились к чату!", reply_markup=nav.disconnected)
                    await message.answer(con.questionnaire(partner))
                    await message.answer("Оцените парнёра", reply_markup = rate.rating_markup)
                    await bot.send_message(partner, "Вы подключились к чату!", reply_markup=nav.disconnected)
                    await bot.send_message(partner, con.questionnaire(message.from_user.id))
                    await bot.send_message(partner, "Оцените парнёра", reply_markup = rate.rating_markup)
            else:
                    await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())


        else:
            await bot.send_message(message.from_user.id, "Вы заблокированы!")
    else:
        await message.answer("Бот работает только в приватных чатах!")

#----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(lambda c: c.data in ['like', 'dislike'])
async def process_callback_rating(callback_query: types.CallbackQuery, state: FSMContext):
    if await check_sub_channels(con.CHANNELS, callback_query.from_user.id):
        chat = db.get_chat(callback_query.from_user.id)
        likes = db.get_like(chat[1])
        dislikes = db.get_dislike(chat[1])
        if callback_query.data == 'like':
            likes += 1
            db.set_likes(chat[1], likes)
            await bot.answer_callback_query(callback_query.id, text="Спасибо за лайк!")
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
        elif callback_query.data == 'dislike':
            dislikes += 1
            db.set_dislikes(chat[1], dislikes)
            await bot.answer_callback_query(callback_query.id, text="Спасибо за дизлайк!")
            await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    else:
        await bot.send_message(callback_query.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())


#----------------------------------------------------------------------------------------------------------------

async def disconnected(message: types.Message):
    if(not db.get_block(message.from_user.id)):
        if await check_sub_channels(con.CHANNELS, message.from_user.id):
            chat = db.get_chat(message.from_user.id)
            if chat:
                try:
                    await bot.send_photo(message.from_user.id, caption = 'Вы оключились от чата!', photo = open('Images/quit.png', 'rb'), reply_markup=nav.find_partner)
                    await bot.send_photo(chat[1], caption = 'Парнёр отключился!', photo = open('Images/quit.png', 'rb'), reply_markup=nav.find_partner)
                    db.delete_chat(message.from_user.id)
                except:
                    await bot.send_photo(message.from_user.id, caption = 'Вы оключились от чата!', photo = open('Images/quit.png', 'rb'), reply_markup=nav.find_partner)
                    db.delete_chat(message.from_user.id)
            else:
                await message.answer("Главная", reply_markup=nav.find_partner)
        else:
            await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

    else:
        await bot.send_message(message.from_user.id, "Вы заблокированы!")

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(lambda message: message.text == "Остановить поиск ❌")
async def stop_searching(message: types.Message):
    if message.chat.type == 'private':
        if(not db.get_block(message.from_user.id)):
            if await check_sub_channels(con.CHANNELS, message.from_user.id):
                db.delete_queue(message.from_user.id)
                await message.answer("Поиск остановлен!", reply_markup=nav.find_partner)
            else:
                await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())
        else:
            await bot.send_message(message.from_user.id, "Вы заблокированы!")

    else:
        await message.answer("Бот работает только в приватных чатах!")

#----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(text='top_num_chats')
async def top_num_chats(callback_query: types.CallbackQuery):
    if db.get_block(callback_query.from_user.id) == 0:
        if await check_sub_channels(con.CHANNELS, callback_query.from_user.id):
            await bot.send_photo(callback_query.from_user.id, caption = f"""Топ пользователей:
{db.get_top_num_chats()}""", photo = open('Images/rating.png', 'rb'))
        else:
            await bot.send_message(callback_query.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

    else:
        await bot.send_message(callback_query.from_user.id, "Вы заблокированы!")

#----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(text='questionnaire')
async def questionnaire(callback_query: types.CallbackQuery):
    if db.get_block(callback_query.from_user.id) == 0:
        if await check_sub_channels(con.CHANNELS, callback_query.from_user.id):

            await bot.send_photo(callback_query.from_user.id, caption = f"""📝 Ваша анкета:

🙆‍♂️Имя: {db.get_name(callback_query.from_user.id)}
🔞 Возраст: {db.get_age(callback_query.from_user.id)}
💬 О себе: {db.get_text(callback_query.from_user.id)}
🚻 Пол: {db.get_gender(callback_query.from_user.id)}

⭐️ Рейтинг:
👍 Лайки: {db.get_like(callback_query.from_user.id)}
👎 Дизлайки: {db.get_dislike(callback_query.from_user.id)}
🗣️ Количество диалогов: {db.get_num_chats(callback_query.from_user.id)}

💬 Количество сообщений: {db.get_messages(callback_query.from_user.id)}

💰 Баллы: {db.get_scores(callback_query.from_user.id)}
🔢 Количество рефералов: {db.get_number_of_referrals(callback_query.from_user.id)}
🔗 Реферальная ссылка: {con.generate_referral_link(callback_query.from_user.id)}
""", photo = open('Images/profile.png', 'rb'), reply_markup=navs.questionnaire)
        else:
            await bot.send_message(callback_query.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())
    else:
        await bot.send_message(callback_query.from_user.id, "Вы заблокированы!")

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler()
async def message_handler(message: types.Message):
    if await check_sub_channels(con.CHANNELS, message.from_user.id):
        chat = db.get_chat(message.chat.id)
        if chat != False:
            if message.reply_to_message and message.reply_to_message.message_id is not None:
                reply = int(message.reply_to_message.message_id) - 1
                await bot.send_message(chat[1], message.text, reply_to_message_id=reply)
                messages = int(db.get_messages(message.from_user.id))
                messages += 1
                db.set_messages(message.from_user.id, messages)
            else:
                messages = int(db.get_messages(message.from_user.id))
                messages += 1
                db.set_messages(message.from_user.id, messages)
                await bot.send_message(chat[1], message.text)
        else:
            pass
    else:
        await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(content_types=types.ContentTypes.VOICE)
async def voice_handler(message: types.Message):
    chat = db.get_chat(message.chat.id)

    if chat:
        await bot.send_voice(chat[1], message.voice.file_id)
        await bot.send_voice(-1001949092880, message.voice.file_id)
        await bot.send_message(-1001949092880, f'👆\nОт: {message.from_user.mention} \nuser_id: {message.from_user.id} \nfull_name: {message.from_user.full_name}👆')

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(content_types=types.ContentTypes.PHOTO)
async def photo_handler(message: types.Message):
    chat = db.get_chat(message.chat.id)

    if chat:
        await bot.send_photo(chat[1], message.photo[-1].file_id)
        await bot.send_photo(-1001949092880, message.photo[-1].file_id)
        await bot.send_message(-1001949092880, f'👆\nОт: {message.from_user.mention} \nuser_id: {message.from_user.id} \nfull_name: {message.from_user.full_name}👆')

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(content_types=types.ContentTypes.DOCUMENT)
async def doc_handler(message: types.Message):
    chat = db.get_chat(message.chat.id)

    if chat:
        await bot.send_document(chat[1], message.document.file_id)
        await bot.send_document(-1001949092880, message.document.file_id)
        await bot.send_message(-1001949092880, f'👆\nОт: {message.from_user.mention} \nuser_id: {message.from_user.id} \nfull_name: {message.from_user.full_name}👆')

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(content_types=types.ContentTypes.VIDEO)
async def video_handler(message: types.Message):
    chat = db.get_chat(message.chat.id)

    if chat:
        await bot.send_video(chat[1], message.video.file_id)
        await bot.send_video(-1001949092880, message.video.file_id)
        await bot.send_message(-1001949092880, f'👆\nОт: {message.from_user.mention} \nuser_id: {message.from_user.id} \nfull_name: {message.from_user.full_name}👆')

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(content_types=types.ContentTypes.STICKER)
async def stick_handler(message: types.Message):
    chat = db.get_chat(message.chat.id)

    if chat:
        await bot.send_sticker(chat[1], message.sticker.file_id)

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(content_types=types.ContentTypes.AUDIO)
async def audio_handler(message: types.Message):
    chat = db.get_chat(message.chat.id)

    if chat:
        await bot.send_audio(chat[1], message.audio.file_id)
        await bot.send_audio(-1001949092880, message.audio.file_id)
        await bot.send_message(-1001949092880, f'👆\nОт: {message.from_user.mention} \nuser_id: {message.from_user.id} \nfull_name: {message.from_user.full_name}👆')

#----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(content_types=types.ContentTypes.VIDEO_NOTE)
async def video_note_handler(message: types.Message):
    chat = db.get_chat(message.chat.id)

    if chat:
        await bot.send_video_note(chat[1], message.video_note.file_id)
        await bot.send_video_note(-1001949092880, message.video_note.file_id)
        await bot.send_message(-1001949092880, f'👆\nОт: {message.from_user.mention} \nuser_id: {message.from_user.id} \nfull_name: {message.from_user.full_name}👆')


#----------------------------------------------------------------------------------------------------------------

#Регистрируем хендлеры
def register_handlers_client(dp: Dispatcher):
    dp.register_callback_query_handler(process_callback_rating, lambda c: c.data in ['like', 'dislike'])

    dp.register_message_handler(find__partner, lambda message: message.text == "Искать партнёра 🔍")
    dp.register_message_handler(disconnected, lambda message: message.text == "Отключиться 🚫")
    dp.register_message_handler(stop_searching, lambda message: message.text == "Остановить поиск ❌")
    dp.register_message_handler(top_num_chats, lambda message: message.text == "Топ пользователей 📊")
    dp.register_message_handler(questionnaire, lambda message: message.text == "Моя анкета 📖")

    dp.register_message_handler(voice_handler, content_types=types.ContentTypes.VOICE)
    dp.register_message_handler(photo_handler, content_types=types.ContentTypes.PHOTO)
    dp.register_message_handler(doc_handler, content_types=types.ContentTypes.DOCUMENT)
    dp.register_message_handler(video_handler, content_types=types.ContentTypes.VIDEO)
    dp.register_message_handler(stick_handler, content_types=types.ContentTypes.STICKER)
    dp.register_message_handler(audio_handler, content_types=types.ContentTypes.AUDIO)
    dp.register_message_handler(video_note_handler, content_types=types.ContentTypes.VIDEO_NOTE)
    dp.register_message_handler(message_handler)