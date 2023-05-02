
    else:
        bot.send_message(message.chat.id, "я тебя не понимаю")


@bot.message_handler()
def det_msg(message):
    bot.send_message(message.chat.id, message.text)

bot.set_my_commands(menu)

if __name__=="__main__":
    bot.polling(none_stop=True, timeout=123, interval=0)