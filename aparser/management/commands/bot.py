import telebot
import sqlite3
import datetime
import time
import json
from django.core.management.base import BaseCommand
from aparser.models import Comics, Users, Films
import os


def check_v(message1):
    sp = read_json('C:/Users/zuiko/OneDrive/Desktop/MarvelBot/data_json/comics.json')['url_comics']['Marvel']
    for i in sp.keys():
        for j in sp[i].keys():
            if j == message1:
                return [i, True]
    return [False]

 
def read_json(path):
    with open(path, "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
        return data


 def Users_in_base(user_id):
    try:
        p = Users.objects.get(user_id=user_id)
        return True
    except Users.DoesNotExist:
        return False


def User_add(user_id, type_user='user', col_proj=0):
    p = Users(
        user_id=user_id,
        type_user=type_user,
        col_proj=col_proj,
    ).save()
    

def Comics_in_base(name):
    try:
        p = Comics.objects.get(name=name)
        return True
    except Comics.DoesNotExist:
        return False

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
        if Comics_in_base(st):
            keyboard_temp.row(st)
    return keyboard_temp



bot = telebot.TeleBot('1417817254:AAGRJdZkQSsNgWZO7Sfp8REFD1aepTPSGJg')


@bot.message_handler(commands=['start'])
def start_message(message):
    if not Users_in_base(message.chat.id):
        User_add(message.chat.id)
    bot.send_message(message.chat.id, 'Привет, в этом боте ты сможешь почитать комиксы Marvel и посмотреть фильмы и сериалы из киновселенной Marvel',
                     reply_markup=keyboard1)
    
 
