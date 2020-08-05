from VkBot import VKBot
import pyowm
from os import getcwd
import threading
from time import sleep, time


token = '29e68d636d84c5971656005a64e1e925a4301cf370acfebe89828c069f7e62e86ae3b64654d7cb3b10fc0'
Bot = VKBot(token = token, id = 189821964)

def game():
    i = 0
    while True:
        sleep(5)
        print(i)
        i += 1

def wait_events():
    for event in Bot.longpoll.listen():
        if Bot.event_is_message(event):
            #Слушаем longpoll, если пришло сообщение то:
            mess = Bot.get_message_text(event).lower()
            if '!инфо' in mess or '!информация' in mess or '!что ты умеешь' in mess or '!info' in mess or '!information' in mess:
                Bot.send_message(peer_id = Bot.get_peer_id(event), message = '"!расписание" - Присылаю расписание на сегодня. Если сегодня не выходной\n\n"!расписание на завтра" - Присылаю расписание на завтра. Если завтра не выходной.\n\n"!все расписание" - Присылаю расписание на неделю группы ВМ(аб)-81\n\n"!анекдот <номер>" - Присылаю анекдот по тематике которая выбирается номером чтобы узнать номера всех тематик команда - "!анекдот"\n\n"!Цитата" - Присылаю случайную цитату\n\n"!рыба текст <число предложений>" - Присылаю текст сгенерированный нейронной сетью с указанным числом предложений\n\n"!покемон имя <имя покемона на англ. языке>" - Присылаю подробную информацию о покемоне имя которого указано\n\n"!покемон номер <номер покемона>" - Присылаю подробную информацию о покемоне номер которого указан\n\n"!гиф <запрос>" - Присылаю гиф картинку по заданному запросу')

            if '!цитата' in mess: #Если написали заданную фразу
                quote = Bot.get_quote()
                if Bot.message_from_user(event): #Если написали в ЛС
                    Bot.send_message(user_id = Bot.get_user_id(event), message = quote)
                elif Bot.message_from_chat(event): #Если написали в Беседе
                    Bot.send_message(chat_id = Bot.get_chat_id(event), message = quote)

            if '!все расписание' in mess or 'всё расписание' in mess:
                Bot.send_message(peer_id = Bot.get_peer_id(event), attachment = Bot.rasp)
                continue

            if '!расписание на завтра' in mess: #Если написали заданную фразу
                week = int(Bot.get_today()) + 1
                if 0 <= week <= 4:
                    Bot.send_message(peer_id = Bot.get_peer_id(event), attachment = Bot.rasp[week])
                elif week == 7:
                    Bot.send_message(peer_id = Bot.get_peer_id(event), attachment = Bot.rasp[0])
                else:
                    Bot.send_message(peer_id = Bot.get_peer_id(event), message = 'Дурашка, мы завтра не учимся!')
                continue

            if '!расписание' in mess: #Если написали заданную фразу
                week = int(Bot.get_today())
                if 0 <= week <= 4:
                    Bot.send_message(peer_id = Bot.get_peer_id(event), attachment = Bot.rasp[week])
                else:
                    Bot.send_message(peer_id = Bot.get_peer_id(event), message = 'Дурашка, мы сегодня не учимся!')

            if '!анекдот ' in mess: #Если написали заданную фразу
                try:
                    num = int(Bot.get_message_text(event)[len('!анекдот ')::])
                    if 1 <= num <= 8 or 11 <= num <= 18:
                        Bot.send_message(peer_id = Bot.get_peer_id(event), message = Bot.get_anekdot(num))
                    else:
                        raise Exception()
                except:
                    Bot.send_message(peer_id = Bot.get_peer_id(event),
                    message = 'Использование команды "анекдот <номер>". Номер:\n1 - Анекдот;\n2 - Рассказы;\n3 - Стишки;\n4 - Афоризмы;\n5 - Цитаты;\n6 - Тосты;\n8 - Статусы;\n11 - Анекдот (+18);\n12 - Рассказы (+18);\n13 - Стишки (+18);\n14 - Афоризмы (+18);\n15 - Цитаты (+18);\n16 - Тосты (+18);\n18 - Статусы (+18)')

            if '!рыба текст ' in mess: #Если написали заданную фразу
                    try:
                        num = int(Bot.get_message_text(event)[len('!рыба текст ')::])
                        if 1 <= num <= 20:
                            Bot.send_message(peer_id = Bot.get_peer_id(event), message = Bot.get_fish_text(num))
                        else:
                            raise Exception()
                    except:
                        Bot.send_message(peer_id = Bot.get_peer_id(event),
                        message = 'Использование команды "рыба текст <число предложений>" 1 <= число предложений <= 20')

            if '!покемон имя ' in mess: #Если написали заданную фразу
                name = Bot.get_message_text(event).lower()[len('!покемон имя ')::]
                pok = Bot.get_pokemon(name=name)
                try:
                    if pok['error']:
                        Bot.send_message(peer_id = Bot.get_peer_id(event), message = 'Видимо такого покемона нет. Использование команды "покемон имя/номер <имя на буржуйском или номер>"')
                except:
                    m = Bot.get_message_pokemon(p=pok[0])
                    Bot.send_message(peer_id = Bot.get_peer_id(event), message = m)

            if '!покемон номер ' in mess: #Если написали заданную фразу
                num = int(Bot.get_message_text(event).lower()[len('!покемон номер ')::])
                pok = Bot.get_pokemon(id=num)
                try:
                    if pok['error']:
                        Bot.send_message(peer_id = Bot.get_peer_id(event), message = 'Видимо такого покемона нет. Использование команды "покемон имя/номер <имя на буржуйском или номер>"')
                except:
                    m = Bot.get_message_pokemon(p=pok[0])
                    Bot.send_message(peer_id = Bot.get_peer_id(event), message = m)

            if '!гиф ' in mess: #Если написали заданную фразу
                q = Bot.get_message_text(event)[len('!гиф ')::]
                url = Bot.get_gif_url(quote=q)
                if url == None:
                    Bot.send_message(peer_id = Bot.get_peer_id(event), message = 'К сожалению ничего не нашлось. Попробуйте изменить запрос.')
                else:
                    with open(getcwd() + '\\imgs\\temp.gif', 'wb') as f:
                        Bot.download(file = f, url = url)
                    doc = Bot.send_doc_to_serv(peer_id = Bot.get_peer_id(event), file = getcwd() + '\\imgs\\temp.gif')
                    Bot.send_message(peer_id = Bot.get_peer_id(event), attachment = 'doc' + str(doc['doc']['owner_id']) + '_' + str(doc['doc']['id']))



events = threading.Thread(target=wait_events)
Game = threading.Thread(target=game)
events.start()
Game.start()
events.join()
Game.join()
