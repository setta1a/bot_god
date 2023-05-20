

from pdf2image import convert_from_path


@bot.message_handler(commands=['pdf2jpg'])
def pdf2jpg_command(message):
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
        if not os.path.exists('files'):
            os.mkdir("files")
        send = bot.send_message(message.chat.id, 'Отправьте pdf файл')
        bot.register_next_step_handler(send, pdf2jpg)
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")


def pdf2jpg(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    except:
        bot.send_message(message.chat.id, 'Вы отправили что-то не то')
        delete_all_tmp_files()
        return
    src = 'files/' + message.document.file_name
    try:
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        pages = convert_from_path(src)
        for i in range(len(pages)):
            pages[i].save('files/page' + str(i) + '.jpg', 'JPEG')
    except:
        bot.send_message(message.chat.id, 'Не могу конвертировать файл')
        delete_all_tmp_files()
        return
    for i in range(len(pages)):
        bot.send_document(message.chat.id, open('files/page' + str(i) + '.jpg', 'rb'))
    delete_all_tmp_files()

menu.append(telebot.types.BotCommand("/pdf2jpg", "Перевод из pdf в jpg файл"))

