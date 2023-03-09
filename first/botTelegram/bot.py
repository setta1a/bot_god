import time
import bs4
import pyowm
import requests
import telebot
import wikipedia
from telebot import TeleBot
from config import config
from telebot import types

wikipedia.set_lang("ru")
bot = TeleBot(config["token"])
owm = pyowm.OWM('7b7c3dcc26c794e9fc67e795781cbcba')




#калькулятор

value = ""
old_value = ""

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton(" ", callback_data="no"),
             telebot.types.InlineKeyboardButton("C", callback_data="C"),
             telebot.types.InlineKeyboardButton(" ", callback_data="no"),
             telebot.types.InlineKeyboardButton("/", callback_data="/"))

keyboard.row(telebot.types.InlineKeyboardButton("7", callback_data="7"),
             telebot.types.InlineKeyboardButton("8", callback_data="8"),
             telebot.types.InlineKeyboardButton("9", callback_data="9"),
             telebot.types.InlineKeyboardButton("×", callback_data="*"))

keyboard.row(telebot.types.InlineKeyboardButton("4", callback_data="4"),
             telebot.types.InlineKeyboardButton("5", callback_data="5"),
             telebot.types.InlineKeyboardButton("6", callback_data="6"),
             telebot.types.InlineKeyboardButton("-", callback_data="-"))

keyboard.row(telebot.types.InlineKeyboardButton("1", callback_data="1"),
             telebot.types.InlineKeyboardButton("2", callback_data="2"),
             telebot.types.InlineKeyboardButton("3", callback_data="3"),
             telebot.types.InlineKeyboardButton("+", callback_data="+"))

keyboard.row(telebot.types.InlineKeyboardButton(" ", callback_data="no"),
             telebot.types.InlineKeyboardButton("0", callback_data="0"),
             telebot.types.InlineKeyboardButton(",", callback_data="."),
             telebot.types.InlineKeyboardButton("=", callback_data="="))
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
#wiki надо найти try accept




def getanekdot():
    z = ''
    s = requests.get('http://anekdotme.ru/random')
    b = bs4.BeautifulSoup(s.text, "html.parser")
    p = b.select('.anekdot_text')
    for x in p:
        s = (x.getText().strip())
        z = z + s + '\n\n'
    return s
@bot.message_handler(commands=["anekdot"])
def anekdot(message):
    bot.send_message(message.from_user.id, getanekdot())



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

@bot.message_handler(commands=["weather"])
def text(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=False)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        lat = message.location.latitude
        lon = message.location.longitude
        observation = owm.weather_at_coords(lat,lon)
        w = str(observation.get_weather()).split(",")
        sde=str(w).split("=")
        bot.reply_to(message, sde[3])
        print(w)




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

