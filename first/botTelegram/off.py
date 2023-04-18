from telebot import types


@bot.message_handler(commands=["off"])
def offer(message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_today = types.KeyboardButton('/да')
    btn_tomorrow = types.KeyboardButton('/нет')
    keyboard_markup.add(btn_today, btn_tomorrow)
    bot.send_message(message.chat.id, 'Ты в этом уверен?', reply_markup=keyboard_markup)


@bot.message_handler(commands=["да"])
def off(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Выключение...",reply_markup=a)
    os.system('shutdown -p')

menu.append(telebot.types.BotCommand("/off", "Выключает компьютер"))