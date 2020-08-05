import vk_api, requests, json, datetime
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from bs4 import BeautifulSoup as bs
from os import getcwd, remove
from pokedex import pokedex
from random import randint


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

    def send_message(self, message = None, peer_id = None, user_id = None, chat_id = None, attachment = None, dont_parse_links=1):
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

    def send_doc_to_serv(self, peer_id, file):
        doc = self.upload.document(doc = file, message_peer_id = peer_id)
        remove(file)
        return doc

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

    def get_fish_text(self, num):
        req = requests.get(url = 'https://fish-text.ru/get', params = {'type' : 'sentence', 'number' : num})
        js = json.loads(req.content)
        return js['text']

    def get_anekdot(self, num):
        req = requests.get(url = 'http://rzhunemogu.ru/RandJSON.aspx?CType=' + str(num))
        return req.content.decode('cp1251')[len('{"content":"'):-2:]

    def get_pokemon(self, name = None, id = None):
        pok = pokedex.Pokedex(version='v1', user_agent='ExampleApp (https://example.com, v2.0.1)')
        if name:
            pokemon = pok.get_pokemon_by_name(name)
        elif id:
            pokemon = pok.get_pokemon_by_number(id)
        return pokemon

    def get_message_pokemon(self, p):
        return f"Номер: {p['number']}\nИмя: {p['name']}\nВид: {p['species']}\nТип: {' '.join(p['types'])}\n     Способности:\nОбычные: {' '.join(p['abilities']['normal'])}\nСкрытые: {' '.join(p['abilities']['hidden'])}\nГруппа яйца: {' '.join(p['eggGroups'])}\nПол: {' '.join(str(i) for i in p['gender'])}\nРост: {p['height']}\nВес: {p['weight']}\nСтадия эволюции: {p['family']['evolutionStage']}\nВсе его эволюции: {' '.join(p['family']['evolutionLine'])}\nСтартовый: {p['starter']}\nЛегендарный: {p['legendary']}\nМифический: {p['mythical']}\nUltra Beast: {p['ultraBeast']}\nMega: {p['mega']}\nФотка: {p['sprite']}\nОписание: {p['description']}"

    def get_gif_url(self, quote):
        key = 'K793Fk3hMprn2nFtY7XiwSyHVsMcgmJX'
        url = 'https://api.giphy.com/v1/gifs/search'
        req = requests.get(url=url, params = {'api_key' : key, 'q' : quote, 'limit' : 50, 'random_id' : key, 'lang' : 'ru'})
        js = json.loads(req.content)
        try:
            return js['data'][randint(0,49)]['images']['original']['url']
        except:
            return None

    def download(self, file, url):
        req = requests.get(url)
        file.write(req.content)
