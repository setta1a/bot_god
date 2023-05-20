

@bot.message_handler(commands=["panda"])
def panda(message):
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
        response = requests.get('https://some-random-api.ml/img/panda')
        url = response.json()['link']
        file = open('history.txt', 'a+')
        file.write(url + '\n')
        bot.send_message(message.from_user.id, url)
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")


menu.append(telebot.types.BotCommand("/panda", "Присылает изображение панды"))

