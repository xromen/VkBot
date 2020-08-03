from VkBot import VKBot


token = '29e68d636d84c5971656005a64e1e925a4301cf370acfebe89828c069f7e62e86ae3b64654d7cb3b10fc0'
Bot = VKBot(token = token, id = 189821964)

for event in Bot.longpoll.listen():
    if Bot.event_is_message(event):
        #Слушаем longpoll, если пришло сообщение то:
        if Bot.get_message_text(event) == 'Цитата': #Если написали заданную фразу
            quote = Bot.get_quote()
            if Bot.message_from_user(event): #Если написали в ЛС
                Bot.send_message(user_id = Bot.get_user_id(event), message = quote)
            elif Bot.message_from_chat(event): #Если написали в Беседе
                Bot.send_message(chat_id = Bot.get_chat_id(event), message = quote)
