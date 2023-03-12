import os
import time
from bs4 import BeautifulSoup
import mouse as mouse
import pyowm
import requests
import telebot
import wikipedia
from telebot import TeleBot
from config import config
from telebot import types
from PIL import Image, ImageGrab, ImageDraw
import platform


wikipedia.set_lang("ru")
bot = TeleBot(config["token"])



#калькулятор

value = ""
old_value = ""

keyboard = telebot.types.InlineKeyboardMarkup()
btn = telebot.types.InlineKeyboardButton
keyboard.row(btn(" ", callback_data="no"), btn("C", callback_data="C"), btn(" ", callback_data="no"), btn("/", callback_data="/"))
keyboard.row(btn("7", callback_data="7"), btn("8", callback_data="8"), btn("9", callback_data="9"), btn("×", callback_data="*"))
keyboard.row(btn("4", callback_data="4"), btn("5", callback_data="5"), btn("6", callback_data="6"), btn("-", callback_data="-"))
keyboard.row(btn("1", callback_data="1"), btn("2", callback_data="2"), btn("3", callback_data="3"), btn("+", callback_data="+"))
keyboard.row(btn(" ", callback_data="no"), btn("0", callback_data="0"), btn(",", callback_data="."), btn("=", callback_data="="))
#вид калькулятора и изменение


@bot.message_handler(commands = ["calculater"])
def getmessages(message):
    global value
    if value == "":
        bot.send_message(message.from_user.id, "0", reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, value, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global value, old_value
    data = query.data
    if data == "no":
        pass
    elif data == "C":
        value = ""
    elif data == "=":
        try:
            value = str(eval(value))
        except:
            value = "Ошибка!"
    else:
        value += data
    if value != old_value:
        if value == "":
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text="0", reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value, reply_markup=keyboard)
    old_value = value
    if value == "Ошибка!": value = ""
#конец калькулятора


#wiki
@bot.message_handler(commands=['wiki'])
def wiki(message):
    try:
        wikipedia.set_lang('ru')
        r = wikipedia.page(message.text.split(maxsplit=1)[1]).content
        sder=r[:1000]
        #цикл остановки отправки до пробела
        if len(sder) > 4096:
            for x in range(0, len(r), 4096):
                bot.send_message(message.chat.id, '{}'.format(r[x:x + 4096]))
                print(x)
        else:
            bot.send_message(message.chat.id, '{}'.format(sder))
    except:
        bot.send_message(message.chat.id, "будь добр написать /wiki 'что желаешь найти'")


def getanekdot():
    r = requests.get('https://www.anekdot.ru/random/anekdot/')
    soup = BeautifulSoup(r.text, 'html.parser')
    anekdot = soup.find_all('div', class_="text")
    for article in anekdot:
        article_title = article.text.strip()
    return article_title


@bot.message_handler(commands=["anekdot"])
def anekdotes(message):
    bot.send_message(message.from_user.id, getanekdot())


@bot.message_handler(commands=["capture"])
def capture_pc(message):
    bot.send_chat_action(message.chat.id, 'upload_photo')
    try:
        currentMouseX, currentMouseY = mouse.get_position()
        img = ImageGrab.grab()
        img.save("screen.png", "png")
        img = Image.open("screen.png")
        draw = ImageDraw.Draw(img)
        draw.polygon(
            (currentMouseX, currentMouseY, currentMouseX, currentMouseY + 15, currentMouseX + 10, currentMouseY + 10),
            fill="white", outline="black")
        img.save("screen_with_mouse.png", "PNG")
        bot.send_photo(message.chat.id, open("screen_with_mouse.png", "rb"))
        os.remove("screen.png")
        os.remove("screen_with_mouse.png")
    except:
        bot.send_message(message.chat.id, "Компьютер заблокирован")


@bot.message_handler(commands=["komp"])
def komp(message):
    req = requests.get('http://ip.42.pl/raw')
    ip = req.text
    uname = os.getlogin()
    windows = platform.platform()
    processor = platform.processor()
    bot.send_message(message.from_user.id, f"*Пользователь:* {uname}\n*IP:* {ip}\n*ОС:* {windows}\n*Процессор:* {processor}", parse_mode="markdown")


@bot.message_handler(commands=["off"])
def offer(message):
    bot.send_message(message.chat.id, "Выключение...")
    os.system('shutdown -p')


@bot.message_handler(commands=["reload"])
def reloader(message):
    bot.send_message(message.chat.id, "Перезагрузка компьютера...")
    os.system('reboot')


@bot.message_handler(commands=["panda"])
def panda(message):
    response = requests.get('https://some-random-api.ml/img/panda')
    url = response.json()['link']
    file = open('history.txt', 'a+')
    file.write(url + '\n')
    bot.send_message(message.from_user.id, url)


@bot.message_handler(commands=["start"])
def hello_user(message):
    greetengs = f"Дарова, <b>{message.from_user.first_name}</b>"
    bot.send_message(message.chat.id, greetengs, parse_mode="html")


@bot.message_handler(commands=["info"])
def get_info(message):
    bot.reply_to(message, f"ваше имя:{message.from_user.first_name}, ваш username: {message.from_user.username}")


count = 0
@bot.message_handler(content_types=["text"])
def chat_bot(message):
    global count
    if message.text.lower() == "сорян":
        count+=1
    elif  message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"И тебе привет, {message.from_user.first_name}!")
    elif message.text.lower() == "как дела?":
        bot.send_message(message.chat.id, "Живой, здоровый, сам как?")
    elif message.text.lower() == "ты бяка":
        for _ in range(200):
            if count == 1:
                bot.send_message(message.chat.id, "я тебя прощаю но только один раз")
                count=2
                break
                # прощает только один раз потом спамит, сделать!!!!!!!!!!
            time.sleep(0.01)
            bot.send_message(message.chat.id, "извинись")
    else:
        bot.send_message(message.chat.id, "я тебя не понимаю")


@bot.message_handler()
def det_msg(message):
    bot.send_message(message.chat.id, message.text)


if __name__=="__main__":
    bot.polling(none_stop=True, timeout=123, interval=0)

