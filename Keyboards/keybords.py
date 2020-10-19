from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


hello_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(KeyboardButton("Поиск по геолокации", request_location=True)).add(KeyboardButton("Поиск по имени"))
