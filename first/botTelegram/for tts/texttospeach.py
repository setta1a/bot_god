from tts import TTS
tts = TTS()


file_path = 'ssr.txt'
client_status = {}

def save(data):
    with open(file_path, 'a') as log_file:
        log_file.write(data)

@bot.message_handler(commands=['tts'])
def begin(message):
    client_id = message.from_user.id
    client_status[client_id] = 'wait_for_data'
    bot.send_message(chat_id=client_id, text='Введите текст который хотите озвучить: ')
