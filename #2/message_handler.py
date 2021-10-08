import re
import requests
import json
import options


def get_answers(type_of_test, test_id):
    url = 'https://uchebnik.mos.ru/exam/rest/secure/testplayer/group'
    payload = json.dumps(
        {'test_type': 'training_test', 'generation_context_type': type_of_test, 'generation_by_id': test_id})
    headers = {'Content-type': 'application/json', 'Cookie': options.cookie}
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json()


async def answers(message_text, send):
    link_to_test = re.findall(r'(selftest/spec|training_spec|test_by_binding)/([\w]+)', message_text)

    type_of_test, test_id = link_to_test[0]
    type_of_test = 'homework' if type_of_test == 'test_by_binding' else 'spec'

    response = get_answers(type_of_test, test_id)
    if 'error' in response:
        return await send("ERROR")

    await send(f'Номер теста {test_id}\nРешаем.. :P')

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
        await send(f'{question}\n\n🙈ОТВЕТ: {right_answer}')


async def unknown(send):
    await send("Я тибя не понима")


async def handler(message_text, send):
    if re.findall(r'(selftest/spec|training_spec|test_by_binding)/([\w]+)', message_text):
        await answers(message_text, send)
    else:
        await unknown(send)
