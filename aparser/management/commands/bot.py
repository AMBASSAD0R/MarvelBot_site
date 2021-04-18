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
    
