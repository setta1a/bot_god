import json
import os
import shutil
import smtplib
from distutils.dir_util import copy_tree
from email.mime.text import MIMEText

from .celerys import app

@app.task
def generate_bot(short_name: str, function_names: list, file_names: list, token: str, bot_os: str, user_name: str):
    file_dir = os.getcwd() + "/staticroot/BOT"
    if os.path.exists(file_dir):
        shutil.rmtree(file_dir)
    os.mkdir(file_dir)

    with open(f"staticroot/BOT/{short_name}.py", "w") as bot:
        with open("first/botTelegram/start_template.py", 'r') as start_file:
            bot.write(start_file.read())
            bot.write(f"USER_DEFAULT = {user_name}")
            bot.write("bot = TeleBot('" + token + "')")

        if "Pdf ==> Docx" in function_names or "Pdf ==> Jpg" in function_names or "MP4 ==> MP3" in function_names:
            with open("first/botTelegram/convert.py", 'r') as convert_file:
                bot.write(convert_file.read())

        for file_name in file_names:
            if file_name in ["stt.py", 'tts.py']:
                if not os.path.exists(os.getcwd() + "/staticroot/BOT/ready"):
                    os.mkdir(os.getcwd() + "/staticroot/BOT/ready")
                if not os.path.exists(os.getcwd() + "/staticroot/BOT/voice"):
                    os.mkdir(os.getcwd() + "/staticroot/BOT/voice")

                if file_name == "stt.py":
                    files = os.listdir(os.getcwd() + "/first/botTelegram/for stt")
                    for fname in files:
                        shutil.copy2(os.path.join("first/botTelegram/for stt", fname), "staticroot/BOT/")

                    with open(f'first/botTelegram/for stt/{file_name}', 'r') as file:
                        code = file.read()
                        bot.write(code)

                elif file_name == "tts.py":
                    files = os.listdir(os.getcwd() + "/first/botTelegram/for tts")
                    if not os.path.exists(os.getcwd() + "/staticroot/BOT/models"):
                        os.mkdir(os.getcwd() + "/staticroot/BOT/models")
                    for fname in files:
                        if os.path.isdir("first/botTelegram/for tts/" + fname):
                            copy_tree("first/botTelegram/for tts/" + fname, "staticroot/BOT/models")
                        else:
                            shutil.copy2(os.path.join("first/botTelegram/for tts", fname), "staticroot/BOT/")

                    with open(f'first/botTelegram/for tts/{file_name}', 'r') as file:
                        code = file.read()
                        bot.write(code)

            else:
                with open(f'first/botTelegram/{file_name}', 'r') as file:
                    code = file.read()
                    bot.write(code)

        with open("first/botTelegram/middle_template.py", 'r') as end_file:
            bot.write(end_file.read())

        if 'Скачать видео/плейлист с Ютуба' in function_names:
            with open("first/botTelegram/yt_text.py", 'r') as end_file:
                bot.write(end_file.read())

        with open("first/botTelegram/end_template.py", 'r') as end_file:
            bot.write(end_file.read())

    cmd = f"pyinstaller --noconfirm --onefile --console --distpath '{os.getcwd()}/staticroot/BOT' '{os.getcwd()}/staticroot/BOT/{short_name}.py'"
    if bot_os == 'win':
        os.chdir("staticroot/BOT")
        cmd = f"docker run -v \"$(pwd):/src/\" batonogov/pyinstaller-windows 'pyinstaller --onefile {short_name}.py'"
    os.system(cmd)

@app.task
def send_email(message, user_email):
    sender = "botgod.sp@gmail.com"
    try:
        with open('../first/email_password.json') as file:
            password = json.load(file)["email_password"]
    except:
        return

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    result_message = f"Пользователь {user_email} отправил сообщение с текстом: {message} \n Ответьте ему как можно быстрее!"
    try:
        print(1)
        server.login(sender, password)
        msg = MIMEText(result_message)
        msg["Subject"] = "ЖАЛОБА ОТ ПОЛЬЗОВАТЕЛЯ"
        server.sendmail(sender, "andreysitalo09@gmail.com", msg.as_string())

        message = '''<!DOCTYPE html>
                                    <html lang="en" style="font-size: 18px; margin: 0; padding: 0;">
                                    <head>
                                        <meta charset="UTF-8">
                                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <title>Message</title>
                                    </head>
                                    <body style="margin: 0; padding: 0;">
                                        <header style="padding: 1%; margin: 0; color: white; background-color: #023653; margin-bottom: 5%;">
                                            <h1 style="margin: auto; text-align: center;">BOTGOD</h1>
                                        </header>
                                        <main style="width: 70%; margin: 0 auto; border: 2px solid #023653; border-radius: 30px; padding: 1%;">
                                            <article>Ваше сообщение очень важно для нас. Оно будет рассмотрено в ближайшее время и на вашу почту будет направлен ответ. С уважением, команда BotGod.</article>
                                        </main>
                                        <footer>

                                        </footer>
                                    </body>
                                    </html>
    '''
        msg = MIMEText(message, 'html')
        msg["Subject"] = "ЖАЛОБА ОТ ПОЛЬЗОВАТЕЛЯ"
        server.sendmail(sender, user_email, msg.as_string())

    except Exception as _ex:
        print(f"{_ex}\nCheck your login or password please!")