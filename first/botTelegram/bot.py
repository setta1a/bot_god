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
from pdf2docx import parse
from typing import Tuple


wikipedia.set_lang("ru")
bot = TeleBot(config["token"])



#функции вставлять сюда

def convert_pdf2docx(input_file: str, output_file: str, pages: Tuple = None):
    """Преобразует PDF в DOCX"""
    if pages:
        pages = [int(i) for i in list(pages) if i.isnumeric()]
    result = parse(pdf_file=input_file, docx_with_path=output_file, pages=pages)
    summary = {
        "Исходный файл": input_file,
        "Страниц": str(pages),
        "Результат преобразования": output_file
    }
    # Печать сводки
    print("#### Отчет ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")
    return result

@bot.message_handler(commands=['pdf2docx'])
def pdf2docx_command(message):
    os.mkdir("files")
    send = bot.send_message(message.chat.id, 'Отправьте pdf файл')
    bot.register_next_step_handler(send, pdf2docx)

def pdf2docx(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'files/' + message.document.file_name
    tmpdocx = open("files/tmpdocx.docx", "w")
    tmpdocx.close()
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    convert_pdf2docx(src, "files/tmpdocx.docx")
    srcdocx = src[0:len(src)-3]+'docx'
    bot.send_document(message.chat.id, open(srcdocx, 'rb'))
    os.remove("files/tmpdocx.docx")
    os.remove(src)
    os.remove(srcdocx)



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
            time.sleep(0.01)
            bot.send_message(message.chat.id, "извинись")
    else:
        bot.send_message(message.chat.id, "я тебя не понимаю")


@bot.message_handler()
def det_msg(message):
    bot.send_message(message.chat.id, message.text)


if __name__=="__main__":
    bot.polling(none_stop=True, timeout=123, interval=0)

