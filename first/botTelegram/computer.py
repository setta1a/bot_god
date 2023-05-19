

@bot.message_handler(commands=["komp"])
def komp(message):
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
        req = requests.get('http://ip.42.pl/raw')
        ip = req.text
        uname = os.getlogin()
        windows = platform.platform()
        processor = platform.processor()
        bot.send_message(message.from_user.id, f"*Пользователь:* {uname}\n*IP:* {ip}\n*ОС:* {windows}\n*Процессор:* {processor}", parse_mode="markdown")
        bot.send_message(message.from_user.id,
                         f"*Пользователь:* {uname}\n*IP:* {ip}\n*ОС:* {windows}\n*Процессор:* {processor}",
                         parse_mode="markdown")
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")


menu.append(telebot.types.BotCommand("/komp", "Высылает информацию о компьютере"))

