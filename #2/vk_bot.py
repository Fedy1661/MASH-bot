import asyncio

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api import VkApi
from functools import partial

import message_handler
import options

vk_session = VkApi(token=options.TOKEN_VK)
# Установка - pip install vk_api
# Переустановка(в слачае проблем) - pip uninstall vk_api
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


async def answer(user_id, text):
    vk_session.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': 0})

print('VK BOT started')
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower()
        send = partial(answer, event.user_id)
        asyncio.run(message_handler.handler(msg, send))
