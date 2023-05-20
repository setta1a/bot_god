from tts import TTS
tts = TTS()


file_path = 'ssr.txt'
client_status = {}

def save(data):
    with open(file_path, 'a') as log_file:
        log_file.write(data)

@bot.message_handler(commands=['tts'])
def begin(message):
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
        client_id = message.from_user.id
        client_status[client_id] = 'wait_for_data'
        bot.send_message(chat_id=client_id, text='Введите текст который хотите озвучить: ')
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")

menu.append(telebot.types.BotCommand("/tts", "Озвучивание текста"))