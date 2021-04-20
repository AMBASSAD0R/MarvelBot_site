import telebot
import sqlite3
import datetime
import time
import json
from django.core.management.base import BaseCommand
from aparser.models import Comics, Users
import os


def check_v(message1):
    sp = read_json('C:/Users/zuiko/OneDrive/Desktop/MarvelBot/data_json/comics.json')['url_comics']['Marvel']
    for i in sp.keys():
        for j in sp[i].keys():
            if j == message1:
                return [i, True]
    return [False]


def read_json(path):
    with open(path, 'r', encoding='utf-8') as read_file:
        data = json.load(read_file)
        return data


def users_in_base(user_id):
    try:
        p = Users.objects.get(user_id=user_id)
        return True
    except Users.DoesNotExist:
        return False


def user_add(user_id, type_user='user', col_proj=0):
    p = Users(
        user_id=user_id,
        type_user=type_user,
        count_reads=col_proj,
    ).save()


def comics_in_base(name):
    try:
        p = Comics.objects.get(name=name)
        return True
    except Comics.DoesNotExist:
        return False


def comics_change(name, col_proj):
    Comics.objects.filter(name=name).update(count_reads=col_proj)


def get_info_comics(name):
    try:
        retro = Comics.objects.filter(name=name)
        return retro.values().get()
    except Comics.DoesNotExist:
        return False


def generate_keyb(keyboard, k, sp):
    for i in sp['url_comics']['Marvel'][k].keys():
        keyboard.row(i)


keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Комиксы')

keyboard_comics = telebot.types.ReplyKeyboardMarkup(True, True)
sp = read_json('C:/Users/zuiko/OneDrive/Desktop/MarvelBot/data_json/comics.json')
for i in sp['url_comics']['Marvel'].keys():
    keyboard_comics.row(i)


def generate_key(name, col):
    keyboard_temp = telebot.types.ReplyKeyboardMarkup(True, True)
    for i in range(0, col):
        st = f'{name} #{i}'
        if comics_in_base(st):
            keyboard_temp.row(st)
    return keyboard_temp


bot = telebot.TeleBot('1417817254:AAGRJdZkQSsNgWZO7Sfp8REFD1aepTPSGJg')


@bot.message_handler(commands=['start'])
def start_message(message):
    if not users_in_base(message.chat.id):
        user_add(message.chat.id)
    bot.send_message(message.chat.id,
                     'Привет, в этом боте ты сможешь почитать комиксы Marvel'
                     ' и посмотреть фильмы и сериалы из киновселенной Marvel',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def comics_video(message):
    global db_comics
    if message.text == 'Комиксы':
        bot.send_message(message.chat.id, 'Тут ты сможешь найти множество комиксов Marvel',
                         reply_markup=keyboard_comics)
    elif message.text == 'В начало':
        bot.send_message(message.chat.id, 'Вы вернулись в начало',
                         reply_markup=keyboard1)
    elif message.text in read_json('C:/Users/zuiko/OneDrive/Desktop/MarvelBot/data_json/comics.json')['url_comics'][
        'Marvel'].keys():
        keybord_c = telebot.types.ReplyKeyboardMarkup(True, True)
        generate_keyb(keybord_c, message.text,
                      read_json('C:/Users/zuiko/OneDrive/Desktop/MarvelBot/data_json/comics.json'))
        keybord_c.row('В начало')
        bot.send_message(message.chat.id, f'Здесь есть множество комиксов из серии {message.text}',
                         reply_markup=keybord_c)
    elif check_v(message.text)[-1] == True:
        com = message.text + ' #'
        keybord_c1 = telebot.types.ReplyKeyboardMarkup(True, True)
        for i in range(1000):
            if comics_in_base(com + str(i)):
                keybord_c1.row(com + str(i))
        keybord_c1.row('В начало')
        bot.send_message(message.chat.id, f'Здесь есть множество выпусков из серии {message.text}',
                         reply_markup=keybord_c1)
    elif comics_in_base(message.text):
        print(get_info_comics(message.text)['cover_id'])
        c = get_info_comics(message.text)['colpage_pdf']
        comics_change(message.text, get_info_comics(message.text)['count_reads'])
        bot.send_photo(message.chat.id, get_info_comics(message.text)['cover_id'],
                       caption=f'{message.text}\nКоличество страниц: {c}')
        bot.send_document(
            message.chat.id, get_info_comics(message.text)['file_id'])
    elif message.text == 'Amazing Spider-Man #1':
        bot.send_document(
            message.chat.id, 'BQACAgIAAxkDAAILlmBKXEkZNZMXjpL89VK7e-HitKVHAAJbDQACpElQSlrX9e3ve4LbHgQ')
    else:
        print(
            message.text in read_json('C:/Users/zuiko/OneDrive/Desktop/MarvelBot/data_json/comics.json')['url_comics'][
                'Marvel'].keys())


class Command(BaseCommand):
    help = 'Запуск бота.'

    def handle(self, *args, **options):
        bot.polling()
