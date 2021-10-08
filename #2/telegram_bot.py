import json
import logging
import re
import requests
import message_handler
from aiogram import Bot, Dispatcher, executor, types
import options

logging.basicConfig(level=logging.INFO)

bot = Bot(token=options.TOKEN_TELEGRAM)
bot.parse_mode = 'html'
dp = Dispatcher(bot)

@dp.message_handler()
async def bot(message: types.Message):
    await message_handler.handler(message.text, message.answer)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
