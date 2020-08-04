from VkBot import VKBot
import pyowm





token = '29e68d636d84c5971656005a64e1e925a4301cf370acfebe89828c069f7e62e86ae3b64654d7cb3b10fc0'
Bot = VKBot(token = token, id = 189821964)
#print(Bot.get_user('xromen')[0]['city'])
for event in Bot.longpoll.listen():
    if Bot.event_is_message(event):
        #Слушаем longpoll, если пришло сообщение то:
        if 'цитата' in Bot.get_message_text(event).lower(): #Если написали заданную фразу
            quote = Bot.get_quote()
            if Bot.message_from_user(event): #Если написали в ЛС
                Bot.send_message(user_id = Bot.get_user_id(event), message = quote)
            elif Bot.message_from_chat(event): #Если написали в Беседе
                Bot.send_message(chat_id = Bot.get_chat_id(event), message = quote)
        if 'все расписание' in Bot.get_message_text(event).lower() or 'всё расписание' in Bot.get_message_text(event).lower():
            Bot.send_message(peer_id = Bot.get_peer_id(event), attachment = Bot.rasp)
            continue
        if 'расписание на завтра' in Bot.get_message_text(event).lower(): #Если написали заданную фразу
            week = int(Bot.get_today()) + 1
            if 0 <= week <= 4:
                Bot.send_message(peer_id = Bot.get_peer_id(event), attachment = Bot.rasp[week])
            elif week == 7:
                Bot.send_message(peer_id = Bot.get_peer_id(event), attachment = Bot.rasp[0])
            else:
                Bot.send_message(peer_id = Bot.get_peer_id(event), message = 'Дурашка, мы завтра не учимся!')
            continue
        if 'расписание' in Bot.get_message_text(event).lower(): #Если написали заданную фразу
            week = int(Bot.get_today())
            if 0 <= week <= 4:
                Bot.send_message(peer_id = Bot.get_peer_id(event), attachment = Bot.rasp[week])
            else:
                Bot.send_message(peer_id = Bot.get_peer_id(event), message = 'Дурашка, мы сегодня не учимся!')
