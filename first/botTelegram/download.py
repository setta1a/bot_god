@bot.message_handler(commands=["download"])
def messc(message):
    bot.send_message(message.from_user.id, "Отправьте необходимый файл")
    bot.register_next_step_handler(message, uploadfile_process)


def uploadfile_process(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.from_user.id, "Файл успешно загружен")
    except:
        bot.send_message(message.from_user.id, "Ошибка! Отправьте файл как документ")
        bot.register_next_step_handler(message, uploadfile_process)

menu.append(telebot.types.BotCommand("/download", "Загрузить файл на компьютер с телеграмм"))