import sys
from os import path

from telebot import types
sys.path.append(path.join(path.dirname(__file__), '..'))

from database import db_aa as db



def keyboard(user_data):
    database = db.Data(user_data)
    table_list = database.table()
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = antiquiz(table_list)
    itembtn2 = tents(table_list)
    itembtn3 = furniture(table_list)
    itembtn4 = casino(table_list)
    markup.add(itembtn1, itembtn2)
    markup.add(itembtn3, itembtn4)
    return markup

def antiquiz(list):
    if (list[2] == False):
        itembtn1 = types.KeyboardButton('Антиквиз')
    else:
        itembtn1 = types.KeyboardButton('Антиквиз ✅')
    return itembtn1


def tents(list):
    if (list[3] == False):
        itembtn2 = types.KeyboardButton('Шатры')
    else:
        itembtn2 = types.KeyboardButton('Шатры ✅')
    return itembtn2

def furniture(list):
    if (list[4] == False):
        itembtn3 = types.KeyboardButton('Мебель')
    else:
        itembtn3 = types.KeyboardButton('Мебель ✅')
    return itembtn3

def casino(list):
    if (list[5] == False):
        itembtn4 = types.KeyboardButton('Казино')
    else:
        itembtn4 = types.KeyboardButton('Казино ✅')
    return itembtn4

def keyboard_back():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Вернуться в меню')
    markup.add(itembtn1)
    return markup


def telegram_quest_inline():
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Телеграм квест','https://arenda-attrakcionov.ru/telegram-kvest-korporativnaya-igra-3/')
    markup.add(itembtn1)
    return markup

def telegram_tent_inline():
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Аренда Шатров','https://arenda-attrakcionov.ru/arenda-shatrov/')
    markup.add(itembtn1)
    return markup

def telegram_furniture_inline():
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Аренда Мебели','https://arenda-attrakcionov.ru/arenda-mebeli/')
    markup.add(itembtn1)
    return markup

def telegram_casino_inline():
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Фан Казино', 'https://arenda-attrakcionov.ru/vyezdnoe-fan-kazino/')
    markup.add(itembtn1)
    return markup

def casino_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Ещё')
    itembtn2 = types.KeyboardButton('Пас')
    markup.add(itembtn1, itembtn2)
    return markup

def keyboard_next():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Далее')
    markup.add(itembtn1)
    return markup

def export():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Экспорт данных')
    markup.add(itembtn1)
    return markup

def crossworld():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Клад')
    itembtn2 = types.KeyboardButton('Кулак')
    itembtn3 = types.KeyboardButton('Скала')
    itembtn4 = types.KeyboardButton('Рулон')
    markup.add(itembtn1, itembtn2)
    markup.add(itembtn3, itembtn4)
    return markup


