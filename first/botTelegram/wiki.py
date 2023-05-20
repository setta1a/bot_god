

@bot.message_handler(commands=['wiki'])
def wiki(message):
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
        try:
            wikipedia.set_lang('ru')
            r = wikipedia.page(message.text.split(maxsplit=1)[1]).content
            sder = r[:1000]
            # цикл остановки отправки до пробела
            if len(sder) > 4096:
                for x in range(0, len(r), 4096):
                    bot.send_message(message.chat.id, '{}'.format(r[x:x + 4096]))
                    print(x)
            else:
                bot.send_message(message.chat.id, '{}'.format(sder))
        except:
            bot.send_message(message.chat.id, "будь добр написать /wiki 'что желаешь найти'")
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")

menu.append(telebot.types.BotCommand("/wiki", "Поиск по слову в википедии"))

