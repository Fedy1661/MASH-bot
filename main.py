import json
import logging
import re

import requests
from aiogram import Bot, Dispatcher, executor, types

import options

logging.basicConfig(level=logging.INFO)

bot = Bot(token=options.token)
bot.parse_mode = 'html'
dp = Dispatcher(bot)


def get_answers(type_of_test, test_id):
    url = 'https://uchebnik.mos.ru/exam/rest/secure/testplayer/group'
    payload = json.dumps(
        {'test_type': 'training_test', 'generation_context_type': type_of_test, 'generation_by_id': test_id})
    headers = {'Content-type': 'application/json', 'Cookie': options.cookie}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


@dp.message_handler()
async def test(message: types.Message):
    link_to_test = re.findall(r'(selftest/spec|training_spec|test_by_binding)/([\w]+)', message.text)

    type_of_test, test_id = link_to_test[0]
    type_of_test = 'homework' if type_of_test == 'test_by_binding' else 'spec'

    response = get_answers(type_of_test, test_id)
    if 'error' in response:
        return await message.answer("ERROR")

    await message.answer(f'Номер теста <b>{test_id}</b>\nРешаем.. :P')

    print(response)

    for task in response['training_tasks']:
        test_task = task['test_task']
        question = test_task['question_elements'][0]['text']
        type_of_question = test_task['answer']['type']
        right_answer = test_task['answer']['right_answer']
        if type_of_question == 'answer/number':
            right_answer = right_answer['number']
        elif type_of_question == 'answer/string':
            right_answer = right_answer['string']
        elif type_of_question == 'answer/single':
            variants = test_task['answer']['options']
            for i in variants:
                if i['id'] in right_answer['id']:
                    right_answer = i['text']
                    break
        else:
            continue
        await message.answer(f'<b>{question}</b>\n\n🙈ОТВЕТ: <i>{right_answer}</i>')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
