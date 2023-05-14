import os
import shutil
from distutils.dir_util import copy_tree

from .celerys import app

@app.task
def generate_bot(short_name: str, function_names: list, file_names: list, token: str, bot_os):
    file_dir = os.getcwd() + "/staticroot/BOT"
    if os.path.exists(file_dir):
        shutil.rmtree(file_dir)
    os.mkdir(file_dir)

    with open(f"staticroot/BOT/{short_name}.py", "w") as bot:
        with open("first/botTelegram/start_template.py", 'r') as start_file:
            bot.write(start_file.read())
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
    if bot_os != 'win':
        cmd = "sudo " + cmd
    os.system(cmd)