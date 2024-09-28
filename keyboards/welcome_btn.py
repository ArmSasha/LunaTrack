from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram import types
from aiogram.types.web_app_info import WebAppInfo

walcome_markup = InlineKeyboardMarkup(row_width=2)
walcome_markup.add(InlineKeyboardButton(text="👨Парень", callback_data="man"),
                  InlineKeyboardButton(text="👩Девушка", callback_data="woman"))


langMenu = InlineKeyboardMarkup(row_width=2)
langMenu.add(InlineKeyboardButton(text='Русский', callback_data='lang_ru'),
            InlineKeyboardButton(text='English', callback_data='lang_en'))

openwebapp = types.InlineKeyboardMarkup()
openwebapp.add(InlineKeyboardButton('Открыть веб страницу', web_app=WebAppInfo(url='https://asoc1al.github.io/LunaTrack/')))