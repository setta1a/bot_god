@bot.message_handler(commands=["off"])
def offer(message):
    bot.send_message(message.chat.id, "Выключение...")
    os.system('shutdown -p')
