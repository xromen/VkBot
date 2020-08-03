import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests
from bs4 import BeautifulSoup as bs
import json



vk_session = vk_api.VkApi(token='29e68d636d84c5971656005a64e1e925a4301cf370acfebe89828c069f7e62e86ae3b64654d7cb3b10fc0')

longpoll = VkBotLongPoll(vk_session, 189821964)
vk = vk_session.get_api()
print('жду')
#print(vk.wall.post(message='Hello world!'))
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
    #Слушаем longpoll, если пришло сообщение то:
        #print(event.raw)
        if event.obj['message']['text'] == 'Цитата': #Если написали заданную фразу

            res = requests.post(url='http://api.forismatic.com/api/1.0/', data = {'method':'getQuote', 'format' : 'json'})
            cit = res.json()['quoteText']
            if event.from_user: #Если написали в ЛС
                vk.messages.send( #Отправляем сообщение
                    user_id=event.obj['message']['from_id'],
                    message=cit,
                    random_id = get_random_id())
            elif event.from_chat: #Если написали в Беседе
                print('Чат')
                vk.messages.send( #Отправляем собщение
                    chat_id=event.chat_id,
                    message=cit,
                    random_id = get_random_id())
