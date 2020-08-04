import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests
from bs4 import BeautifulSoup as bs
import json
from os import getcwd
import datetime


class VKBot:
    def __init__(self, token, id):
        self.token = token
        self.vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkBotLongPoll(self.vk_session, id)
        self.vk = self.vk_session.get_api()
        self.upload = vk_api.VkUpload(self.vk_session)
        self.rasp = ['photo249134825_457243139', 'photo249134825_457243140', 'photo249134825_457243141', 'photo249134825_457243142', 'photo249134825_457243143']

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

    def send_message(self, message = None, peer_id = None, user_id = None, chat_id = None, attachment = None):
        print(f'send message {message} to user:{user_id} or chat:{chat_id} or peer: {peer_id}')
        self.vk.messages.send( #Отправляем сообщение
            user_id=user_id,
            chat_id=chat_id,
            peer_id = peer_id,
            message=message,
            attachment = attachment,
            random_id = get_random_id())

    def send_img_to_serv(self, peer_id, week):
        print(f'send photo message to {peer_id}')
        photo = self.upload.photo_messages(photos = getcwd() + '\\imgs\\' + str(week) + '.png', peer_id = peer_id)
        return photo

    def send_img_message(self, peer_id, week):
        photo = send_img_to_serv(peer_id = peer_id, week = week)
        self.send_message(peer_id = str(peer_id), attachment = 'photo' + str(photo[0]['owner_id']) + '_' + str(photo[0]['id']))

    def get_user_id(self, event):
        return event.obj['message']['from_id']

    def get_chat_id(self, event):
        return event.chat_id

    def get_peer_id(self, event):
        return int(event.obj['message']['peer_id'])

    def get_user(self, id):
        return self.vk.users.get(user_ids=id, fields = ['city'])

    def get_today(self):
        return datetime.date.weekday(datetime.date.today())
