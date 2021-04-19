import requests
import os
from fake_useragent import UserAgent
import time
import glob
import img2pdf
import PyPDF2
from bs4 import BeautifulSoup
import json
import telebot
import sqlite3
from django.core.management.base import BaseCommand
from aparser.models import Comics



def generate_headers():
    ua = UserAgent()
    return {'user-agent': ua.random}


def img_to_pdf_one(path1, path2):
    try:
        path = path1 + '/' + path2
        if not os.path.exists(f'{path}/{path2}.pdf'):
            with open(f'{path}/{path2}.pdf', "wb") as f:
                f.write(img2pdf.convert(glob.glob(path + "\*.jpg")))
    except Exception as e:
        print(e)
