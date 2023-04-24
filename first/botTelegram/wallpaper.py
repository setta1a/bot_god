import ctypes


@bot.message_handler(commands=["wallpaper"])
def wallpaper(message):
    msg = bot.send_message(message.chat.id, "Отправьте картинку:")
    bot.register_next_step_handler(msg, set_wallpaper)


@bot.message_handler(content_types=["photo"])
def set_wallpaper(message):
    file = message.photo[-1].file_id
    file = bot.get_file(file)
    download_file = bot.download_file(file.file_path)
    with open("image.jpg", "wb") as img:
        img.write(download_file)
    path = os.path.abspath("image.jpg")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)

menu.append(telebot.types.BotCommand("/wallpaper", "Заменяет обои на рабочем столе"))