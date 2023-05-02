

@bot.message_handler(commands=["panda"])
def panda(message):
    response = requests.get('https://some-random-api.ml/img/panda')
    url = response.json()['link']
    file = open('history.txt', 'a+')
    file.write(url + '\n')
    bot.send_message(message.from_user.id, url)

menu.append(telebot.types.BotCommand("/panda", "Присылает изображение панды"))

