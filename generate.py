from first.models import BotFunctions


def generate():
    with open("BOT.py", "w") as bot:
        functions = BotFunctions.objects.all()
        for func in functions:
            with open(f'botTelegram/{func.file_name}', 'r') as file:
                code = file.read()
                bot.write(code)


if __name__ == '__main__':
    generate()
