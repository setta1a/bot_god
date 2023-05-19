import os
import telebot
import time
from bs4 import BeautifulSoup
import mouse as mouse
import requests
import wikipedia
from telebot import TeleBot
from PIL import Image, ImageGrab, ImageDraw
import subprocess
import platform
import json
menu=[]

bot = TeleBot('6168841765:AAFy82jbAY9hh6juk8J6kRNQ8jId8G246a0')

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

menu.append(telebot.types.BotCommand("/wiki", "Поиск по слову в википедии"))

@bot.message_handler(commands=["start"])
def hello_user(message):
    greetengs = f"Дарова, <b>{message.from_user.first_name}</b>"
    bot.send_message(message.chat.id, greetengs, parse_mode="html")

menu.append(telebot.types.BotCommand("/start", "Приветствует пользователя"))

@bot.message_handler(commands=["info"])
def get_info(message):
    bot.reply_to(message, f"ваше имя:{message.from_user.first_name}, ваш username: {message.from_user.username}")


@bot.message_handler(commands=["нет"])
def off(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Ну и фиг с тобой",reply_markup=a)

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
            time.sleep(0.01)
            bot.send_message(message.chat.id, "извинись")

    else:
        bot.send_message(message.chat.id, "я тебя не понимаю")


@bot.message_handler()
def det_msg(message):
    bot.send_message(message.chat.id, message.text)

bot.set_my_commands(menu)

if __name__=="__main__":
    bot.polling(none_stop=True, timeout=123, interval=0)
