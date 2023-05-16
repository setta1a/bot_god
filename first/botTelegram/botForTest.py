import os
import telebot
import time
import requests
import wikipedia
from telebot import TeleBot
from PIL import ImageGrab
import subprocess
import platform

from first.botTelegram import config

menu = []
bot = TeleBot(config["token"])
# Сюда:
# anekdot

from bs4 import BeautifulSoup


def getanekdot():
    r = requests.get('https://nekdo.ru/random/')
    soup = BeautifulSoup(r.text, "html.parser")
    joke_text = soup.find('div', class_='text').get_text()
    return joke_text


@bot.message_handler(commands=["anekdot"])
def anekdotes(message):
    bot.send_message(message.from_user.id, getanekdot())


menu.append(telebot.types.BotCommand("/anekdot", "Высылает анекдот"))

# apis
import json

apis = []


def load_api():
    if os.path.isfile('api.json') == False:
        tmp = open("api.json", "w+")
        tmp.write("[]")
        tmp.close()
    with open('api.json', 'r') as f:
        data = f.read()
        data = json.loads(data)
    return data


def save_api():
    with open('api.json', 'w') as f:
        json.dump(apis, f)


# функции вставлять сюда
@bot.message_handler(commands=["add_api"])
def add_api(message):
    new_api = {
        "name": None,
        "command": None,
        "url": None,
        "keys": []
    }
    send = bot.send_message(message.chat.id, 'Напишите название функции')
    bot.register_next_step_handler(send, add_api_step2, new_api)


def add_api_step2(message, new_api):
    new_api['name'] = message.text
    send = bot.send_message(message.chat.id, 'Напишите название команды вызова')
    bot.register_next_step_handler(send, add_api_step3, new_api)


def add_api_step3(message, new_api):
    new_api['command'] = message.text
    send = bot.send_message(message.chat.id, 'Вставьте сслыку на API')
    bot.register_next_step_handler(send, add_api_step35, new_api)


def add_api_step35(message, new_api):
    new_api['url'] = message.text
    send = bot.send_message(message.chat.id,
                            'Напишите передаваемые параметры через пробел (name=Anton param1=100500) или - если их нет')
    bot.register_next_step_handler(send, add_api_step4, new_api)


def add_api_step4(message, new_api):
    new_api['params'] = message.text
    send = bot.send_message(message.chat.id, 'Напишите название значения')
    bot.register_next_step_handler(send, add_api_step5, new_api)


def add_api_step5(message, new_api):
    new_api['keys'].append({"name": message.text, "path": ""})
    send = bot.send_message(message.chat.id,
                            'Напишите путь до значения (hello.world.[3].name #названия в пути разделены точками, в [] записываются индексы для массивов)')
    bot.register_next_step_handler(send, add_api_step6, new_api)


def add_api_step6(message, new_api):
    new_api['keys'][-1]["path"] = message.text
    send = bot.send_message(message.chat.id,
                            'Напишите "сохранить", чтобы сохранить api или "добавить", чтобы добавить еще значение для вывода')
    bot.register_next_step_handler(send, add_api_step7, new_api)


def add_api_step7(message, new_api):
    if (message.text.lower() == 'добавить'):
        send = bot.send_message(message.chat.id, 'Напишите название значения')
        bot.register_next_step_handler(send, add_api_step5, new_api)
    else:
        apis.append(new_api)
        save_api()
        bot.send_message(message.chat.id, 'API сохранено')


@bot.message_handler(commands=["run_api"])
def run_api(message):
    text = list(message.text.split())[-1].lower()
    run = -1
    for i in range(len(apis)):
        api = apis[i]
        if api["name"].lower() == text or api["command"].lower() == text:
            run = i
            break
    if run != -1:
        try:
            run = apis[i]
            try:
                payload = {}
                if run["params"] != '-':
                    params = list(run["params"].split())
                    for param in params:
                        key, val = param.split('=')
                        payload[key] = val
                    data = requests.get(run["url"], params=payload)
                else:
                    data = requests.get(run["url"])
            except:
                data = requests.get(run["url"])
            data = data.json()
            out = f'{run["name"]}\n'
            count = 1
            for param in run["keys"]:
                path = list(param["path"].split("."))
                for j in range(len(path)):
                    if path[j][0] == '[':
                        new_part = ""
                        for i in range(1, len(path[j])):
                            if (path[j][i] == ']'):
                                break
                            else:
                                new_part += path[j][i]
                        path[j] = int(new_part)
                val = data
                try:
                    for part in path:
                        val = val[part]
                except:
                    val = "undefined"
                out += f"{count}. {param['name']}: {val} \n"
                count += 1
            bot.send_message(message.chat.id, out)
        except:
            bot.send_message(message.chat.id, "API не работает")
    else:
        bot.send_message(message.chat.id, "Такого API нет")


@bot.message_handler(commands=["list_api"])
def list_api(message):
    out = "Список APi: \n"
    count = 1
    for api in apis:
        out += str(count) + '. name: ' + api["name"] + '; command: ' + api["command"] + ';\n'
        count += 1
    if (out == ""):
        bot.send_message(message.chat.id, "Пока нет не одного API")
    else:
        bot.send_message(message.chat.id, out)


@bot.message_handler(commands=["delete_api"])
def delete_api(message):
    text = list(message.text.split())[-1].lower()
    to_remove = -1
    for i in range(len(apis)):
        api = apis[i]
        if api["name"].lower() == text or api["command"].lower() == text:
            to_remove = i
            break
    if (to_remove != -1):
        deleted_name = apis[to_remove]["name"]
        apis.pop(to_remove)
        tmp = f"API {deleted_name} успешно удалено"
        bot.send_message(message.chat.id, tmp)
        save_api()
    else:
        bot.send_message(message.chat.id, "Такого API нет")


menu.append(telebot.types.BotCommand("/add_api", "Добавить API"))
menu.append(telebot.types.BotCommand("/run_api", "Запустить API"))
menu.append(telebot.types.BotCommand("/list_api", "Показать список API"))
menu.append(telebot.types.BotCommand("/delete_api", "Удалить API"))

# capture
from sys import platform

import pyautogui


@bot.message_handler(commands=["capture"])
def capture_pc(message):
    if platform.system() == "Windows":
        bot.send_chat_action(message.chat.id, 'upload_photo')
        try:
            filename = f"{time.time()}.jpg"
            pyautogui.screenshot(filename)
            with open(filename, "rb") as img:
                bot.send_photo(message.chat.id, img)
            os.remove(filename)
        except:
            bot.send_message(message.chat.id, "Что-то пошло не так")
    elif platform.system() == "Linux":
        try:
            img = ImageGrab.grab()
            img.save("screenshot.jpg", quality="web_medium")
            photo = open('screenshot.jpg', 'rb')
            bot.send_photo(message.chat.id, photo)
            photo.close()
            os.remove('screenshot.jpg')
        except:
            bot.send_message(message.chat.id, 'Что-то пошло не так')


menu.append(telebot.types.BotCommand("/capture", "Высылает скриншот с экрана компьютера"))


# computer
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
    bot.send_message(message.from_user.id,
                     f"*Пользователь:* {uname}\n*IP:* {ip}\n*ОС:* {windows}\n*Процессор:* {processor}",
                     parse_mode="markdown")


menu.append(telebot.types.BotCommand("/komp", "Высылает информацию о компьютере"))


# convert
def delete_all_tmp_files():
    dir = 'files'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))


# download


@bot.message_handler(commands=["download"])
def messc(message):
    bot.send_message(message.from_user.id, "Отправьте необходимый файл")
    bot.register_next_step_handler(message, uploadfile_process)


def uploadfile_process(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.send_message(message.from_user.id, "Файл успешно загружен")
    except:
        bot.send_message(message.from_user.id, "Ошибка! Отправьте файл как документ")
        bot.register_next_step_handler(message, uploadfile_process)


menu.append(telebot.types.BotCommand("/download", "Загрузить файл на компьютер с телеграмм"))

# mp42mp3


from moviepy.editor import VideoFileClip


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
    mp3_src = src[0:len(src) - 1] + '3'
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


menu.append(telebot.types.BotCommand("/mp42mp3", "Перевод из mp4 в mp3 файл"))


# off
@bot.message_handler(commands=["off"])
def offer(message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_today = types.KeyboardButton('/да')
    btn_tomorrow = types.KeyboardButton('/нет')
    keyboard_markup.add(btn_today, btn_tomorrow)
    bot.send_message(message.chat.id, 'Ты в этом уверен?', reply_markup=keyboard_markup)


@bot.message_handler(commands=["да"])
def off(message):
    a = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Выключение...", reply_markup=a)
    if platform.system() == "Windows":
        os.system('shutdown -p')
    elif platform.system() == "Linux":
        subprocess.Popen(['shutdown', '-h', 'now'])


menu.append(telebot.types.BotCommand("/off", "Выключает компьютер"))


# panda


@bot.message_handler(commands=["panda"])
def panda(message):
    response = requests.get('https://some-random-api.ml/img/panda')
    url = response.json()['link']
    file = open('history.txt', 'a+')
    file.write(url + '\n')
    bot.send_message(message.from_user.id, url)


menu.append(telebot.types.BotCommand("/panda", "Присылает изображение панды"))

# pdf2docx


from typing import Tuple
from pdf2docx import parse


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
    srcdocx = src[0:len(src) - 3] + 'docx'
    bot.send_document(message.chat.id, open(srcdocx, 'rb'))
    delete_all_tmp_files()


menu.append(telebot.types.BotCommand("/pdf2docx", "Перевод из pdf в docx файл"))

# pdf2jpg


from pdf2image import convert_from_path


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


menu.append(telebot.types.BotCommand("/pdf2jpg", "Перевод из pdf в jpg файл"))

# reload


from telebot import types


@bot.message_handler(commands=["reload"])
def reloader(message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_today = types.KeyboardButton('/конечно')
    btn_tomorrow = types.KeyboardButton('/нет')
    keyboard_markup.add(btn_today, btn_tomorrow)
    bot.send_message(message.chat.id, 'Ты в этом уверен?', reply_markup=keyboard_markup)


@bot.message_handler(commands=["конечно"])
def f(message):
    bot.send_message(message.chat.id, "Перезагрузка компьютера...")
    if platform.system() == "Windows":
        os.system('reboot')
    elif platform.system() == "Linux":
        subprocess.check_call(['systemctl', 'reboot', '-i'])


menu.append(telebot.types.BotCommand("/reload", "Перезгрузка компьютера"))


# upload


@bot.message_handler(commands=["upload"])
def messc(message):
    bot.send_message(message.from_user.id, "Укажите путь до файла: ")
    bot.register_next_step_handler(message, downfile_process)


def downfile_process(message):
    bot.send_chat_action(message.from_user.id, 'typing')
    try:
        file_path = message.text
        if os.path.exists(file_path):
            bot.send_message(message.from_user.id, "Файл загружается, подождите...")
            bot.send_chat_action(message.from_user.id, 'upload_document')
            file_doc = open(file_path, 'rb')
            bot.send_document(message.from_user.id, file_doc)
        else:
            bot.send_message(message.from_user.id,
                             "Файл не найден или указан неверный путь (ПР.: C:\\Documents\\File.doc)")
    except:
        bot.send_message(message.from_user.id,
                         "Ошибка! Файл не найден или указан неверный путь (ПР.: C:\\Documents\\File.doc)")


menu.append(telebot.types.BotCommand("/upload", "Загрузить файл c компьютера в телеграмм"))

# wallpaper


import ctypes


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


menu.append(telebot.types.BotCommand("/wallpaper", "Заменяет обои на рабочем столе"))

# webcam


import cv2


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


menu.append(telebot.types.BotCommand("/webcam", "Присылает изображение с камеры"))


# wiki


@bot.message_handler(commands=['wiki'])
def wiki(message):
    try:
        wikipedia.set_lang('ru')
        r = wikipedia.page(message.text.split(maxsplit=1)[1]).content
        sder = r[:1000]
        # цикл остановки отправки до пробела
        if len(sder) > 4096:
            for x in range(0, len(r), 4096):
                bot.send_message(message.chat.id, '{}'.format(r[x:x + 4096]))
                print(x)
        else:
            bot.send_message(message.chat.id, '{}'.format(sder))
    except:
        bot.send_message(message.chat.id, "будь добр написать /wiki 'что желаешь найти'")


menu.append(telebot.types.BotCommand("/wiki", "Поиск по слову в википедии"))

# yt


from pytube import YouTube
from pytube import Playlist
import datetime
import re


def writes_logs(_ex):
    """Записывает логи в файл 'logs.log', в котором будет время и ошибка"""
    with open('logs.log', 'a') as file_log:
        file_log.write('\n' + str(datetime.datetime.now()) + ': ' + str(_ex))


def create_audio(url):
    """Скачивает и открывает файл на бинарное чтение"""
    try:
        yt = YouTube(url).streams.get_highest_resolution()
        path = yt.download("music")
        audio = open(path, 'rb')
        return audio
    except Exception as _ex:
        writes_logs(_ex)


def delete_all_music_in_directory():
    """Удаляет все скаченные аудио из папки 'music'"""
    if not os.path.exists('music'):
        os.mkdir('music')
    for file in os.listdir('music'):
        try:
            if re.search('mp4', file):
                mp4_path = os.path.join('music', file)
                os.remove(mp4_path)
        except Exception as _ex:
            writes_logs(_ex)


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
    bot.send_message(message.chat.id, "Ну и фиг с тобой", reply_markup=a)


count = 0


@bot.message_handler(content_types=["text"])
def chat_bot(message):
    global count
    if message.text.lower() == "сорян":
        count += 1
    elif message.text.lower() == "привет":
        bot.send_message(message.chat.id, f"И тебе привет, {message.from_user.first_name}!")
    elif message.text.lower() == "как дела?":
        bot.send_message(message.chat.id, "Живой, здоровый, сам как?")
    elif message.text.lower() == "ты бяка":
        for _ in range(200):
            if count == 1:
                bot.send_message(message.chat.id, "я тебя прощаю но только один раз")
                count = 2
                break
            time.sleep(0.01)
            bot.send_message(message.chat.id, "извинись")
    # yt_text
    elif message.text[:38] == 'https://www.youtube.com/playlist?list=':
        # Для плейлиста
        playlist = Playlist(message.text)
        for url in playlist:
            try:
                audio = create_audio(url)
                bot.send_audio(message.chat.id, audio)
                bot.register_next_step_handler(delete_all_music_in_directory())
            except Exception as _ex:
                writes_logs(_ex)
        else:
            bot.send_message(message.chat.id, "Плейлист закрыт")

    elif message.text[:32] == 'https://www.youtube.com/watch?v=' or message.text[:17] == 'https://youtu.be/':
        # Для видео
        try:
            url = message.text
            audio = create_audio(url)
            bot.send_video(message.chat.id, audio)
            bot.register_next_step_handler(delete_all_music_in_directory())
        except Exception as _ex:
            writes_logs(_ex)

    # yt_text_end
    else:
        bot.send_message(message.chat.id, "я тебя не понимаю")


@bot.message_handler()
def det_msg(message):
    bot.send_message(message.chat.id, message.text)


bot.set_my_commands(menu)

if __name__ == "__main__":
    bot.polling(none_stop=True, timeout=123, interval=0)
