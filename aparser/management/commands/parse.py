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
