@bot.message_handler(commands=['lock'])
def loker(message):
    bot.send_message(message.chat.id, "Происходит блокировка компьютера...")
    if platform.system() == "Windows":
        os.system("rundll32.exe user32.dll, LockWorkStation")
    elif platform.system() == "Linux":
        subprocess.Popen('loginctl lock-sessio')
    bot.send_message(message.chat.id, "Компьютер заблокирован!")


menu.append(telebot.types.BotCommand("/lock", "Вызывает блокировку экрана компьютера"))