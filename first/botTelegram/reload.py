

from telebot import types


@bot.message_handler(commands=["reload"])
def reloader(message):
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
        keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        btn_today = types.KeyboardButton('/конечно')
        btn_tomorrow = types.KeyboardButton('/нет')
        keyboard_markup.add(btn_today, btn_tomorrow)
        bot.send_message(message.chat.id, 'Ты в этом уверен?', reply_markup=keyboard_markup)
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")

@bot.message_handler(commands=["конечно"])
def f(message):
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
        bot.send_message(message.chat.id, "Перезагрузка компьютера...")
        if platform.system() == "Windows":
            os.system('reboot')
        elif platform.system() == "Linux":
            subprocess.check_call(['systemctl', 'reboot', '-i'])
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")


menu.append(telebot.types.BotCommand("/reload", "Перезгрузка компьютера"))

