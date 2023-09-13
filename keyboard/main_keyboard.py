import sys
from os import path

from telebot import types
sys.path.append(path.join(path.dirname(__file__), '..'))

from database import db_aa as db



def keyboard(user_data):
    database = db.Data(user_data)
    table_list = database.table()
    table_list = table_list[2:]
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = air1(table_list)
    itembtn2 = air2(table_list)
    itembtn3 = water1(table_list)
    itembtn4 = water2(table_list)
    itembtn5 = fire1(table_list)
    itembtn6 = fire2(table_list)
    itembtn7 = fire3(table_list)
    itembtn8 = earth1(table_list)
    itembtn9 = earth2(table_list)
    itembtn10 = earth3(table_list)

    markup.add( itembtn5, itembtn6, itembtn7)
    markup.add(itembtn1, itembtn2)
    markup.add(itembtn8, itembtn9, itembtn10)
    markup.add(itembtn3, itembtn4)
    return markup

def air1(list):
    if (list[0] == False or list[1] == False):
        itembtn1 = types.KeyboardButton('Воздух 1')
    else:
        itembtn1 = types.KeyboardButton('Воздух 1 ✅')
    return itembtn1

def air2(list):
    if (list[6] == False or list[7] == False):
        itembtn2 = types.KeyboardButton('Воздух 2')
    else:
        itembtn2 = types.KeyboardButton('Воздух 2 ✅')
    return itembtn2


def water1(list):
    if (list[8] == False or list[9] == False):
        itembtn3 = types.KeyboardButton('Вода 1')
    else:
        itembtn3 = types.KeyboardButton('Вода 1 ✅')
    return itembtn3

def water2(list):
    if (list[10] == False or list[11] == False):
        itembtn4 = types.KeyboardButton('Вода 2')
    else:
        itembtn4 = types.KeyboardButton('Вода 2 ✅')
    return itembtn4

def fire1(list):
    if (list[4] == False or list[5] == False):
        itembtn5 = types.KeyboardButton('Огонь 1')
    else:
        itembtn5 = types.KeyboardButton('Огонь 1 ✅')
    return itembtn5

def fire2(list):
    if (list[14] == False or list[15] == False):
        itembtn6 = types.KeyboardButton('Огонь 2')
    else:
        itembtn6 = types.KeyboardButton('Огонь 2 ✅')
    return itembtn6

def fire3(list):
    if (list[18] == False or list[19] == False):
        itembtn7 = types.KeyboardButton('Огонь 3')
    else:
        itembtn7 = types.KeyboardButton('Огонь 3 ✅')
    return itembtn7

def earth1(list):
    if (list[2] == False or list[3] == False):
        itembtn8 = types.KeyboardButton('Земля 1')
    else:
        itembtn8 = types.KeyboardButton('Земля 1 ✅')
    return itembtn8

def earth2(list):
    if (list[14] == False or list[15] == False):
        itembtn9 = types.KeyboardButton('Земля 2')
    else:
        itembtn9 = types.KeyboardButton('Земля 2 ✅')
    return itembtn9

def earth3(list):
    if (list[18] == False or list[19] == False):
        itembtn10 = types.KeyboardButton('Земля 3')
    else:
        itembtn10 = types.KeyboardButton('Земля 3 ✅')
    return itembtn10

def keyboard_back():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Вернуться в меню')
    markup.add(itembtn1)
    return markup

def keyboard_miss():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Пропустить')
    markup.add(itembtn1)
    return markup

def export():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Экспорт данных')
    markup.add(itembtn1)
    return markup


