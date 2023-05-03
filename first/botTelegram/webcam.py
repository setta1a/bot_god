

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

