

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
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
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
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")




@bot.message_handler(commands=["list_api"])
def list_api(message):
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
        out = "Список APi: \n"
        count = 1
        for api in apis:
            out += str(count) + '. name: ' + api["name"] + '; command: ' + api["command"] + ';\n'
            count += 1
        if (out == ""):
            bot.send_message(message.chat.id, "Пока нет не одного API")
        else:
            bot.send_message(message.chat.id, out)
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")



@bot.message_handler(commands=["delete_api"])
def delete_api(message):
    user_id = message.from_user.username
    if user_id == USER_DEFAULT:
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
    else:
        bot.send_message(message.chat.id, "Вы не тот пользователь")



menu.append(telebot.types.BotCommand("/add_api", "Добавить API"))
menu.append(telebot.types.BotCommand("/run_api", "Запустить API"))
menu.append(telebot.types.BotCommand("/list_api", "Показать список API"))
menu.append(telebot.types.BotCommand("/delete_api", "Удалить API"))

