

from bs4 import BeautifulSoup


def getanekdot():
    r = requests.get('https://nekdo.ru/random/')
    soup = BeautifulSoup(r.text, "html.parser")
    joke_text = soup.find('div', class_='text').get_text()
    return joke_text


@bot.message_handler(commands=["anekdot"])
def anekdotes(message):
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
        bot.send_message(message.from_user.id, getanekdot())
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")

menu.append(telebot.types.BotCommand("/anekdot", "Высылает анекдот"))

