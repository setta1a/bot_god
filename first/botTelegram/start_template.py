import os
import time
from bs4 import BeautifulSoup
import mouse as mouse
import requests
import wikipedia
from telebot import TeleBot
from PIL import Image, ImageGrab, ImageDraw
import platform
import json
with open('config.json') as json_file:
    config = json.load(json_file)
wikipedia.set_lang("ru")
bot = TeleBot(config["token"])