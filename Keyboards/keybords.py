from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


hello_keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)\
    .add(InlineKeyboardButton("Поиск по геолокации", callback_data="location", request_location=True))\
    .add(InlineKeyboardButton("Поиск по имени", callback_data="name"))

def artist_name_keyboard(arists: list):
    keyboard = InlineKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for artist in arists:
        keyboard.add(InlineKeyboardButton(artist["Name"], callback_data=artist["Artist_code"]))
    return keyboard