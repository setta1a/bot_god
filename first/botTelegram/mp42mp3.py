

from moviepy.editor import VideoFileClip


def converttomp3(mp4file, mp3file):
    video = VideoFileClip(mp4file)
    # получаем аудиодорожку
    audio = video.audio
    # сохраняем аудио файл
    audio.write_audiofile(mp3file)
    # уничтожаем объекты
    # что бы не было ошибок
    audio.close()
    video.close()


@bot.message_handler(commands=['mp42mp3'])
def mp42pm3_command(message):
    if not os.path.exists('files'):
        os.mkdir("files")
    send = bot.send_message(message.chat.id, 'Отправьте mp4 файл')
    bot.register_next_step_handler(send, mp42pm3)


def mp42pm3(message):
    try:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    except:
        bot.send_message(message.chat.id, 'Вы отправили что-то не то')
        delete_all_tmp_files()
        return
    src = 'files/' + message.video.file_name
    mp3_src = src[0:len(src) - 1] + '3'
    tmpmp3 = open(mp3_src, "w")
    tmpmp3.close()
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    try:
        converttomp3(src, mp3_src)
    except:
        bot.send_message(message.chat.id, 'Не могу конвертировать файл')
        delete_all_tmp_files()
        return
    bot.send_document(message.chat.id, open(mp3_src, 'rb'))
    delete_all_tmp_files()


menu.append(telebot.types.BotCommand("/mp42mp3", "Перевод из mp4 в mp3 файл"))

