import os
import time
import json
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



wikipedia.set_lang("ru")
bot = TeleBot(config["token"])
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

#функции вставлять сюда
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
    send = bot.send_message(message.chat.id, 'Напишите передаваемые параметры через пробел (name=Anton param1=100500) или - если их нет')
    bot.register_next_step_handler(send, add_api_step4, new_api)

def add_api_step4(message, new_api):
    new_api['params'] = message.text
    send = bot.send_message(message.chat.id, 'Напишите название значения')
    bot.register_next_step_handler(send, add_api_step5, new_api)

def add_api_step5(message, new_api):
    new_api['keys'].append({"name": message.text, "path" : ""})
    send = bot.send_message(message.chat.id, 'Напишите путь до значения (hello.world.[3].name #названия в пути разделены точками, в [] записываются индексы для массивов)')
    bot.register_next_step_handler(send, add_api_step6, new_api)

def add_api_step6(message, new_api):
    new_api['keys'][-1]["path"] = message.text
    send = bot.send_message(message.chat.id, 'Напишите "сохранить", чтобы сохранить api или "добавить", чтобы добавить еще значение для вывода')
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
                            if(path[j][i] == ']'):
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
    if(out == ""):
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
    if(to_remove != -1):
        deleted_name = apis[to_remove]["name"]
        apis.pop(to_remove)
        tmp = f"API {deleted_name} успешно удалено"
        bot.send_message(message.chat.id, tmp)
        save_api()
    else:
        bot.send_message(message.chat.id, "Такого API нет")


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
    apis = load_api()
    bot.polling(none_stop=True, timeout=123, interval=0)

