import os
import time
from bs4 import BeautifulSoup
import mouse as mouse
import requests
import telebot
import wikipedia
from telebot import TeleBot
from config import config
from telebot import types
from PIL import Image, ImageGrab, ImageDraw
import platform
import cv2
import ctypes
from pdf2docx import parse
from typing import Tuple
from pdf2image import convert_from_path
from moviepy.editor import VideoFileClip
import pyautogui as pyautogui


wikipedia.set_lang("ru")
bot = TeleBot(config["token"])


def delete_all_tmp_files():
    dir = 'files'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


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
    if not os.path.exists('files'):
        os.mkdir("files")
    send = bot.send_message(message.chat.id, 'Отправьте pdf файл')
    bot.register_next_step_handler(send, pdf2docx)


def pdf2docx(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    except:
        bot.send_message(message.chat.id, 'Вы отправили что-то не то')
        delete_all_tmp_files()
        return
    src = 'files/' + message.document.file_name
    tmpdocx = open("files/tmpdocx.docx", "w")
    tmpdocx.close()
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    try:
        convert_pdf2docx(src, "files/tmpdocx.docx")
    except:
        bot.send_message(message.chat.id, 'Не могу конвертировать файл')
        delete_all_tmp_files()
        return
    srcdocx = src[0:len(src)-3]+'docx'
    bot.send_document(message.chat.id, open(srcdocx, 'rb'))
    delete_all_tmp_files()


@bot.message_handler(commands=['pdf2jpg'])
def pdf2jpg_command(message):
    if not os.path.exists('files'):
        os.mkdir("files")
    send = bot.send_message(message.chat.id, 'Отправьте pdf файл')
    bot.register_next_step_handler(send, pdf2jpg)

def pdf2jpg(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    except:
        bot.send_message(message.chat.id, 'Вы отправили что-то не то')
        delete_all_tmp_files()
        return
    src = 'files/' + message.document.file_name
    try:
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        pages = convert_from_path(src)
        for i in range(len(pages)):
            pages[i].save('files/page' + str(i) + '.jpg', 'JPEG')
    except:
        bot.send_message(message.chat.id, 'Не могу конвертировать файл')
        delete_all_tmp_files()
        return
    for i in range(len(pages)):
        bot.send_document(message.chat.id, open('files/page' + str(i) + '.jpg', 'rb'))
    delete_all_tmp_files()


def converttomp3(mp4file, mp3file):
    video = VideoFileClip(mp4file)
    # получаем аудиодорожку
    audio = video.audio
    # сохраняем аудио файл
    audio.write_audiofile(mp3file)
    # уничтожаем объекты
    # что бы не было ошибок
    audio.close()
    video.close()


@bot.message_handler(commands=['mp42mp3'])
def mp42pm3_command(message):
    if not os.path.exists('files'):
        os.mkdir("files")
    send = bot.send_message(message.chat.id, 'Отправьте mp4 файл')
    bot.register_next_step_handler(send, mp42pm3)


def mp42pm3(message):
    try:
        file_info = bot.get_file(message.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    except:
        bot.send_message(message.chat.id, 'Вы отправили что-то не то')
        delete_all_tmp_files()
        return
    src = 'files/' + message.video.file_name
    mp3_src = src[0:len(src)-1] + '3'
    tmpmp3 = open(mp3_src, "w")
    tmpmp3.close()
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    try:
        converttomp3(src, mp3_src)
    except:
        bot.send_message(message.chat.id, 'Не могу конвертировать файл')
        delete_all_tmp_files()
        return
    bot.send_document(message.chat.id, open(mp3_src, 'rb'))
    delete_all_tmp_files()


@bot.message_handler(commands=["panda"])
def panda(message):
    response = requests.get('https://some-random-api.ml/img/panda')
    url = response.json()['link']
    file = open('history.txt', 'a+')
    file.write(url + '\n')
    bot.send_message(message.from_user.id, url)


@bot.message_handler(commands=["off"])
def offer(message):
    bot.send_message(message.chat.id, "Выключение...")
    os.system('shutdown -p')


@bot.message_handler(commands=["komp"])
def komp(message):
    req = requests.get('http://ip.42.pl/raw')
    ip = req.text
    uname = os.getlogin()
    windows = platform.platform()
    processor = platform.processor()
    bot.send_message(message.from_user.id,
                     f"*Пользователь:* {uname}\n*IP:* {ip}\n*ОС:* {windows}\n*Процессор:* {processor}",
                     parse_mode="markdown")


@bot.message_handler(commands=["capture"])
def capture_pc(message):
    bot.send_chat_action(message.chat.id, 'upload_photo')
    try:
        filename = f"{time.time()}.jpg"
        pyautogui.screenshot(filename)
        with open(filename, "rb") as img:
            bot.send_photo(message.chat.id, img)
        os.remove(filename)
    except:
        bot.send_message(message.chat.id, "Компьютер заблокирован")


def getanekdot():
    r = requests.get('https://nekdo.ru/random/')
    soup = BeautifulSoup(r.text, "html.parser")
    joke_text = soup.find('div', class_='text').get_text()
    return joke_text


@bot.message_handler(commands=["anekdot"])
def anekdotes(message):
    bot.send_message(message.from_user.id, getanekdot())


@bot.message_handler(commands=["wallpaper"])
def wallpaper(message):
    msg = bot.send_message(message.chat.id, "Отправьте картинку:")
    bot.register_next_step_handler(msg, set_wallpaper)


@bot.message_handler(content_types=["photo"])
def set_wallpaper(message):
    file = message.photo[-1].file_id
    file = bot.get_file(file)
    download_file = bot.download_file(file.file_path)
    with open("image.jpg", "wb") as img:
        img.write(download_file)
    path = os.path.abspath("image.jpg")
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


@bot.message_handler(commands=["webcam"])
def webcam(message):
    try:
        filename = "cam.jpg"
        cap = cv2.VideoCapture(0)
        for i in range(30):
            cap.read()
        ret, frame = cap.read()
        cv2.imwrite(filename, frame)
        cap.release()
        with open(filename, "rb") as img:
            bot.send_photo(message.chat.id, img)
        os.remove(filename)
    except:
        bot.send_message(message.chat.id, "Камера отсутствует или неисправна")


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

