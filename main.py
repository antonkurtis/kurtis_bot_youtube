import urllib
from urllib import request
from urllib.parse import quote
import re
from random import randint
import telebot
import config
import database

bot = telebot.TeleBot(config.token)

last_search = []


def findvideo(x):
    data1 = []
    url = 'https://www.youtube.com/results?search_query=' + quote(x)
    links = urllib.request.urlopen(url).read().decode('cp1251', errors='ignore')
    match = re.findall("\?v\=(.+?)\"", links)
    if not (match is None):
        for i in match:
            if (len(i) < 25):
                data1.append(i)
    data1 = dict(zip(data1, data1)).values()
    data2 = []
    for y in data1:
        data2.append('https://www.youtube.com/watch?v=' + y)
    return data2


pict = [
    'https://station.ru/uploads/eb/a8/d64ae18b34ad4f5b72df2545aab0.jpg',
    'https://magickum.com/wp-content/uploads/2018/10/photo_2018-10-01_17-23-28.jpg',
    'https://banner2.cleanpng.com/20180604/swg/kisspng-youtube-video-computer-icons-santa-barbara-5b14eb442a3d10.876269151528097604173.jpg',
    'https://i.pinimg.com/originals/19/7b/36/197b365922d1ea3aa1a932ff9bbda4a6.png'
]


@bot.message_handler(commands=["start"])
def cmd_start(message):
    database.set_state(message.chat.id, config.States.S_START.value)
    bot.send_message(message.chat.id, "Привет, я Youtube Бот  \n"
                                      "Введите /info для того, что бы узнать ,чем я могу помочь Вам.\n"
                                      "Введите /commands для списка доступных комманд.\n"
                                      "Введите /reset для начала нового диалога.")
    bot.send_photo(message.chat.id, pict[randint(0, 3)])
    database.set_state(message.chat.id, config.States.S_CHOICE.value)


@bot.message_handler(commands=["reset"])
def cmd_reset(message):
    bot.send_message(message.chat.id, "Давайте начнем с начала.\n"
                                      "Используйте /info или /commands для того чем и как Я могу помочь.")
    database.set_state(message.chat.id, config.States.S_CHOICE.value)
    global last_search
    last_search = []


@bot.message_handler(commands=["find_video"])
def cmd_find_video(message):
    bot.send_message(message.chat.id, 'Введите слово/фразу для поиска')
    @bot.message_handler(content_types=["text"])
    def cmd_search_video(message):
        global last_search
        last_search = findvideo(message.text)
        print_result(message.chat.id)


@bot.message_handler(commands=["get_trending"])
def cmd_get_trending(message):
    bot.send_message(message.chat.id, 'https://www.youtube.com/feed/trending')


@bot.message_handler(commands=["last_search"])
def cmd_last_search(message):
    if len(last_search) <= 0:
        bot.send_message(message.chat.id, "Нет данных о последнем поиске")
    else:
        print_result(message.chat.id)


def print_result(id):
    counter = 0
    for j in last_search:
        counter += 1
        if counter < 11:
            bot.send_message(id, j)
        else:
            break


@bot.message_handler(commands=["info"])
def cmd_info(message):
    bot.send_message(message.chat.id, "Я поисковый бот Youtube.\n"
                                      "Помогу с поиском видео по ключевым словам.\n"
                                      "Введите /reset для старта с начала.")


@bot.message_handler(commands=["commands"])
def cmd_commands(message):
    bot.send_message(message.chat.id, "/reset - используется для сброса предыдущих поисков и старта с начала.\n"
                                      "/start - используется для старта диалога и начала работы.\n"
                                      "/info - информация о том, чем Я могу помочь Вам.\n"
                                      "/commands - Список комманд и инфо, для чего они используются.\n"
                                      "/find_video - используется для поиска видео.\n"
                                      "/get_trending - используется для отображения видео в тренде на сегодня.\n"
                                      "/last_search - используется для повтора последнего поиска")


if __name__ == "__main__":
    bot.infinity_polling()
