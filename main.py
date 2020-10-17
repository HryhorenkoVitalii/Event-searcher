import logging
from aiogram import Bot, Dispatcher, executor, types
import os


API_TOKEN = os.getenv("Concert_Bot_API")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Я помогу тебе найти ближайшие концерты твоих любимых исполнителей по всему земному шару.\n Введи имя артиста")


@dp.message_handler()
async def echo(message: types.Message):
    await FormToAdd.keyword.set()
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
