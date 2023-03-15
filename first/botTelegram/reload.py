@bot.message_handler(commands=["reload"])
def reloader(message):
    bot.send_message(message.chat.id, "Перезагрузка компьютера...")
    os.system('reboot')