from telebot import types

@bot.message_handler(commands=["reload"])
def reloader(message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_today = types.KeyboardButton('/конечно')
    btn_tomorrow = types.KeyboardButton('/нет')
    keyboard_markup.add(btn_today, btn_tomorrow)
    bot.send_message(message.chat.id, 'Ты в этом уверен?', reply_markup=keyboard_markup)

@bot.message_handler(commands=["конечно"])
def f(message):
    bot.send_message(message.chat.id, "Перезагрузка компьютера...")
    os.system('reboot')

menu.append(telebot.types.BotCommand("/reload", "Перезгрузка компьютера"))