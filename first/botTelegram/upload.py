

@bot.message_handler(commands=["upload"])
def messc(message):
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
        bot.send_message(message.from_user.id, "Укажите путь до файла: ")
        bot.register_next_step_handler(message, downfile_process)
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")


def downfile_process(message):
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
        bot.send_chat_action(message.from_user.id, 'typing')
        try:
            file_path = message.text
            if os.path.exists(file_path):
                bot.send_message(message.from_user.id, "Файл загружается, подождите...")
                bot.send_chat_action(message.from_user.id, 'upload_document')
                file_doc = open(file_path, 'rb')
                bot.send_document(message.from_user.id, file_doc)
            else:
                bot.send_message(message.from_user.id, "Файл не найден или указан неверный путь (ПР.: C:\\Documents\\File.doc)")
        except:
            bot.send_message(message.from_user.id, "Ошибка! Файл не найден или указан неверный путь (ПР.: C:\\Documents\\File.doc)")
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")


menu.append(telebot.types.BotCommand("/upload", "Загрузить файл c компьютера в телеграмм"))

