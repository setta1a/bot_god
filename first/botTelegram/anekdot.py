def getanekdot():
    r = requests.get('https://nekdo.ru/random/')
    soup = BeautifulSoup(r.text, "html.parser")
    joke_text = soup.find('div', class_='text').get_text()
    return joke_text


@bot.message_handler(commands=["anekdot"])
def anekdotes(message):
    bot.send_message(message.from_user.id, getanekdot())
