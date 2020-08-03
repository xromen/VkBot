import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests
from bs4 import BeautifulSoup as bs
import json


class VKBot:
    def __init__(self, token, id):
        self.token = token
        self.vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.vk_session, id)
        self.vk = self.vk_session.get_api()

    def get_quote(self):
        print('Parsing quote')
        res = requests.post(url='http://api.forismatic.com/api/1.0/', data = {'method':'getQuote', 'format' : 'json'})
        quote = res.json()['quoteText']
        return quote

    def event_is_message(self, event):
        return event.type == VkBotEventType.MESSAGE_NEW

    def get_message_text(self, event):
        return event.obj['message']['text']

    def message_from_user(self, event):
        return event.from_user

    def message_from_chat(self, event):
        return event.from_chat

    def send_message(self, message, user_id = None, chat_id = None):
        print(f'send message {message} to user:{user_id} or chat:{chat_id}')
        self.vk.messages.send( #Отправляем сообщение
            user_id=user_id,
            chat_id=chat_id,
            message=message,
            random_id = get_random_id())

    def get_user_id(self, event):
        return event.obj['message']['from_id']

    def get_chat_id(self, event):
        return event.chat_id
