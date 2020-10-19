import logging
from aiogram import Bot, Dispatcher, executor, types
import handlers
from Keyboards.keybords import hello_keyboard
from config import API_TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "Я помогу тебе найти ближайшие концерты по всему земному шару.\n Выбери тип поиска",
                           reply_markup=hello_keyboard)

@dp.message_handler()
async def echo(message: types.Message):
    result = handlers.name_artist(message.text)
    await message.answer(result)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
