from create_bot import dp, bot, db, check_sub_channels
from keyboards import menu_btn as nav
from keyboards import client_btn as navs
import config as con
from aiogram import types, Dispatcher
from states import FCMPromo
from aiogram.dispatcher import FSMContext

# #----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(lambda message: message.text == "Магазин🛍")
async def back_main(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	if(not db.get_block(callback_query.from_user.id)):
		if await check_sub_channels(con.CHANNELS, callback_query.from_user.id):
		
			await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
			await bot.send_message(callback_query.from_user.id, 'Меню🏠', reply_markup=navs.find_partner)
        
		else:
			await bot.send_message(callback_query.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

	else:
		await bot.send_message(callback_query.from_user.id, "Вы заблокированы!")

# #----------------------------------------------------------------------------------------------------------------

# #----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(lambda message: message.text == "Магазин🛍")
async def shop(message: types.Message):
	if(not db.get_block(message.from_user.id)):
		if await check_sub_channels(con.CHANNELS, message.from_user.id):

			await bot.send_message(message.from_user.id, 'В разработке')

		else:
			await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

	else:
		await bot.send_message(message.from_user.id, "Вы заблокированы!")

# #----------------------------------------------------------------------------------------------------------------



# @dp.callback_query_handler(text='achievements')
async def achievements(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	if db.get_block(callback_query.from_user.id) == 0:
		if await check_sub_channels(con.CHANNELS, callback_query.from_user.id):

			await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

			await bot.send_message(callback_query.from_user.id, 'Выберите действие:', reply_markup=nav.achievements)
	        
		else:
			await bot.send_message(callback_query.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

	else:
	    await bot.send_message(callback_query.from_user.id, "Вы заблокированы!")

# #----------------------------------------------------------------------------------------------------------------
# #----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(text='quantity_messages')
async def quantity_messages(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	if db.get_block(callback_query.from_user.id) == 0:
		if await check_sub_channels(con.CHANNELS, callback_query.from_user.id):

			await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

			messages = int(db.get_messages(callback_query.from_user.id))

			if messages >= 100:
				# Вычисляем баллы за 100 сообщений
				scores = int(db.get_scores(callback_query.from_user.id))
				scores += 50
				db.set_scores(callback_query.from_user.id, scores)
				await bot.send_message(callback_query.from_user.id, f"Ты получил 50 баллов за 100 сообщений! \nТвой текущий счет: {db.get_scores(callback_query.from_user.id)} баллов.", reply_markup=nav.achievements)
				messages -= 100
				db.set_messages(callback_query.from_user.id, messages)
			else:
				messages_to_add = 100 - (messages % 100)
				await bot.send_message(callback_query.from_user.id, f"Тебе не хватает {messages_to_add} сообщений для получения баллов. \nТвой текущий счет: {db.get_scores(callback_query.from_user.id)} баллов.", reply_markup=nav.achievements)
		else:
		    await bot.send_message(callback_query.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

	else:
	    await bot.send_message(callback_query.from_user.id, "Вы заблокированы!")

# #----------------------------------------------------------------------------------------------------------------
# #----------------------------------------------------------------------------------------------------------------

# @dp.callback_query_handler(text='promo_code')
async def promo(callback_query: types.CallbackQuery):
	await bot.answer_callback_query(callback_query.id)
	if db.get_block(callback_query.from_user.id) == 0:
		if await check_sub_channels(con.CHANNELS, callback_query.from_user.id):

			await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

			await bot.send_message(callback_query.from_user.id, 'Введите промокод')
			await FCMPromo.code.set()
		else:
			await bot.send_message(callback_query.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

	else:
	    await bot.send_message(callback_query.from_user.id, "Вы заблокированы!")

# #----------------------------------------------------------------------------------------------------------------

# @dp.message_handler(state=FCMPromo.code)
async def promo_code(message: types.Message, state: FSMContext):
    if db.get_block(message.from_user.id) == 0:
	    if await check_sub_channels(con.CHANNELS, message.from_user.id):

	        code = message.text

	        # Проверка существования промокода и оставшихся активаций
	        if db.existence_promo(code):
	            # Проверка, использовал ли пользователь промокод ранее
	            user_id = message.from_user.id

	            # Проверка, использовал ли пользователь промокод ранее
	            if db.check_used_promo(user_id, code):
	                await message.reply("Вы уже активировали этот промокод ранее.", reply_markup=nav.achievements)
	            else:
	                # Отметить промокод как использованный данным пользователем
	                db.add_used_promo(user_id, code)

	                # Получить количество баллов для этого промокода
	                promo_points = db.get_promo_points(code)

	                # Начислить баллы пользователю
	                scores = int(db.get_scores(user_id))
	                scores += promo_points
	                db.set_scores(user_id, scores)

	                # Уменьшить количество оставшихся активаций на 1
	                db.minus_usage_promo(code)  # Передайте код промокода

	                # Отправить уведомление о успешной активации промокода и начисленных баллах
	                await bot.send_message(user_id, 'Промокод успешно активирован!')
	                await bot.send_message(user_id, f"Вы получили {promo_points} баллов за активацию промокода. "
	                                               f"Ваш текущий счет: {db.get_scores(user_id)} баллов.",
	                                      reply_markup=nav.achievements)
	        else:
	            await message.reply("Данный промокод не существует или количество его использований исчерпано.", reply_markup=nav.achievements)

	        await state.finish()
	    else:
	        await bot.send_message(message.from_user.id, con.NOT_SUB_MESSAGE, reply_markup=sub.showChannels())

    else:
        await bot.send_message(message.from_user.id, "Вы заблокированы!")
        await state.finish()

#----------------------------------------------------------------------------------------------------------------

#Регистрируем хендлеры
def register_handlers_menu(dp: Dispatcher):
	dp.register_callback_query_handler(back_main, text='back_main')
	dp.register_message_handler(shop, lambda message: message.text == "Магазин🛍")
	dp.register_callback_query_handler(achievements, text='achievements')
	dp.register_callback_query_handler(quantity_messages, text='quantity_messages')
	dp.register_callback_query_handler(promo, text='promo_code')
	dp.register_message_handler(promo_code, state=FCMPromo.code)
