import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from Keyboards.keybords import hello_keyboard, artist_name_keyboard
from Parsers.scraper import search_artist
from config import API_TOKEN



logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

start, choice, name = range(3)
user_state = {}


def get_state(message):
    return user_state[message.from_user.id]


@dp.message_handler(commands=['start'])
async def welcome(message: types.Message):
    user_state[message.chat.id] = start
    await bot.send_message(message.from_user.id,
                           "Я помогу тебе найти ближайшие концерты по всему земному шару.Выбери тип поиска",
                           reply_markup=hello_keyboard)


@dp.callback_query_handler(lambda x: x.data == "name")
async def search_from_name(message):
    user_state[message.from_user.id] = name
    await bot.send_message(message.from_user.id, "Введите имя артиста")

@dp.message_handler(lambda message: get_state(message) == name)
async def name_result(message):
    artist_list = search_artist(message.text)
    if len(artist_list) == 1:
        user_state[message.from_user.id] = choice
        image = "http://images.sk-static.com/images/media/profile_images/artists/219230/large_avatar"
        await bot.send_photo(message.from_user.id, image)
    elif len(artist_list) == 0:
        user_state[message.from_user.id] = name
        await bot.send_message(message.from_user.id, "Повторите ввод, по вашему запросу ничего не найдено.")
    else:
        user_state[message.from_user.id] = choice
        keyboard = artist_name_keyboard(artist_list)
        await bot.send_message(message.from_user.id, "Найдено несколько артистов.", reply_markup=keyboard)

@dp.message_handler(lambda message: get_state(message) == choice)
async def choice_name(message):
    print(2)
    await bot.send_message(message.from_user.id, message.text)







@dp.callback_query_handler(lambda x: x.data == "location")
async def search_from_location(message):
    await bot.send_message(message.from_user.id, message)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
