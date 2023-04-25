@bot.message_handler(commands=["start"])
def hello_user(message):
    greetengs = f"Дарова, <b>{message.from_user.first_name}</b>"
    bot.send_message(message.chat.id, greetengs, parse_mode="html")

menu.append(telebot.types.BotCommand("/start", "Приветствует пользователя"))

@bot.message_handler(commands=["info"])
def get_info(message):
    bot.reply_to(message, f"ваше имя:{message.from_user.first_name}, ваш username: {message.from_user.username}")


@bot.message_handler(commands=["нет"])
def off(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Ну и фиг с тобой",reply_markup=a)

count = 0
@bot.message_handler(content_types=["text"])
def chat_bot(message):
    global count
    if message.text.lower() == "сорян":
        count+=1
    elif  message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"И тебе привет, {message.from_user.first_name}!")
    elif message.text.lower() == "как дела?":
        bot.send_message(message.chat.id, "Живой, здоровый, сам как?")
    elif message.text.lower() == "ты бяка":
        for _ in range(200):
            if count == 1:
                bot.send_message(message.chat.id, "я тебя прощаю но только один раз")
                count=2
                break
            time.sleep(0.01)
            bot.send_message(message.chat.id, "извинись")
