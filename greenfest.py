import random
import telebot
from datetime import datetime
from telebot import types
import time
import os
from telebot.types import InputFile
import re
import json

import keyboard.main_keyboard as keyboard
import database.db_aa as db
from Export.export import export_data

bot = telebot.TeleBot('6537930874:AAF2-_i2wtR_fECWv3JANrofBLMOibG-WzE')


def timeppp(message):
    newTimeString = datetime.fromtimestamp(message).strftime('%H:%M:%S - %d %b %Z')
    print(newTimeString)


def text_check(text):
    import re
    regex = re.compile('[^a-zA-Zа-яА-Я0-9]')
    return regex.sub('', text)


incorrect = ['Хм.. даю ещё шанс 😊',
             'Предлагаю поразмыслить ещё',
             'Нуууу... не то, увы',
             'Так-так-так, почти! Но нет!',
             'Давай-давай! Я в тебя верю!',
             ]
menedjer = 64783167
menedjer_1 = 703608663

admin_id = '703608663'


# 703608663
# 64783167

# def handle_callback_query(message):
#     source = None
#     if len(message.text.split()) > 1:
#         source = message.text.split()[1]
#
#     # Determine where the user came from
#     if source == 'source_qr':
#         # User came from a QR code
#         bot.reply_to(message, 'Welcome! You came from a QR code.')
#     elif source == 'source_link':
#         # User came from a link
#         bot.reply_to(message, 'Welcome! You came from a link.')
#     else:
#         # User did not come from a QR code or link
#         bot.reply_to(message, 'Welcome!')

# -------------Начало---------------------------
@bot.message_handler(commands=['start'])
def handle_start(message):
    if (message.from_user.id == menedjer):
        bot.send_message(message.chat.id, 'Вам доступен экспорт', reply_markup=keyboard.export())
    else:
        info = db.Data(message.from_user)
        info.create()
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEIHd1kDu6_l3UN8qquRGL97sxH0shhzAACGCwAAnCfWEhLkKAVEv7IwC8E")
        bot.send_message(message.chat.id, '_Привет, дорогой друг! БЛА БЛА БЛА_\n'
                                          '\n'
                                          '_Мы подготовили для тебя квест. Впереди интересные загадки на логику, а также '
                                          'активности, которые расположены по всей территории._', parse_mode="Markdown")
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEIHd1kDu6_l3UN8qquRGL97sxH0shhzAACGCwAAnCfWEhLkKAVEv7IwC8E")
        bot.send_message(message.chat.id,
                         "_Прежде, чем мы начнём, расскажу об игре. Всё очень просто:_\n"
                         "\n"
                         "_1. Каждый играет сам за себя, при желании  можно объединиться в пары. "
                         "Бот будет работать с 11:00 до 16:00\n"
                         "\n"
                         "2. Войти в игру можно в рамках указанного времени, также есть возможность поставить её на "
                         "паузу и продолжить позднее!\n"
                         "\n"
                         "3. Ты получишь меню с десятью заданиями. Выбирай любое и нажимай на него\n"
                         "\n"
                         "4. Я пришлю карту с обозначением точки оффлайн-активности \n"
                         "\n"
                         "5. Когда придешь на точку, проводник даст тебе оффлайн-задание\n"
                         "\n"
                         "6. После его прохождения проводник скажет кодовое слово, которое надо написать в чат\n"
                         "\n"
                         "7. После кода, я пришлю тебе логическое задание. Ответ впиши в чат\n"
                         "\n"
                         "8. После выполнения задания одной ценности появится галочка о прохождении\n"
                         "\n"
                         "9. Задание можно пропустить и вернуться в меню\n"
                         "\n"
                         "За прохождение всех заданий, ты получишь 10 Гринкоинов,но для этого нам нужно познакомиться\n"
                         "\n"
                         "По любым вопросам обращайся:_ [@blacklist_event](@blacklist_event)\n"
                         "\n"
                         "_Если всё понятно, введи свою_ *фамилию*", parse_mode="Markdown")
        bot.register_next_step_handler(message, surname)
        # bot.send_message(64783167, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')
        # bot.send_message(1248171558, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')
        # bot.send_message(483241197, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')


@bot.message_handler(func=lambda message: message.text.lower() == 'экспорт данных', content_types=['text'])
def export(message):
    try:
        if (message.from_user.id == menedjer):
            excel_name = export_data()
            print(excel_name)
            bot.send_document(message.chat.id, InputFile(excel_name))
            os.remove(excel_name)
    except Exception as error:
        print(f'export: {error}')


@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'animation', 'voice'])
def take(message):
    print(message)
    bot.delete_message(message.chat.id, message.message_id)


# -------------Ввод имени---------------------------
def surname(message):
    try:
        if message.content_type == 'text':
            collector(message)
            set_surname(message)
            bot.send_message(message.chat.id,
                             "_Отлично! Теперь_ *имя*", parse_mode="Markdown")
            bot.register_next_step_handler(message, name)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, '_Надо ввести_ *фамилию*\n',
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, surname)
    except Exception as error:
        print(f'surname: {error}')
        bot.register_next_step_handler(message, surname)


# -------------Ввод телефона---------------------------
def name(message):
    try:
        if message.content_type == 'text':
            set_name(message)
            bot.send_message(message.chat.id,
                             "_Великолепно! И последнее –_ *номер телефона*", parse_mode="Markdown")
            bot.register_next_step_handler(message, start)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, '_Надо ввести_ *имя*\n',
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, name)
    except Exception as error:
        print(f'name: {error}')
        bot.register_next_step_handler(message, name)


# -------------Начало---------------------------
def start(message):
    try:
        if message.content_type == 'text':
            set_phone(message)
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEIHzFkDzxFeaWhNjihFqQaSFaZNWMzSAACWyoAAvMreEibkHdAfD2kCS8E")
            bot.send_message(message.chat.id, '_Лето – уникальная пора, когда даже самый заядлый домосед выбирается '
                                              'на природу и в путешествия. Именно там можно получить нестандартный опыт,'
                                              ' который может пригодиться. Вот только сейчас портал в лето закрыт!\n'
                                              '\n'
                                              'Мы предлагаем отправиться еще в одно путешествие, столкнуться со всеми '
                                              'стихиями и приручить их! Ведь есть сходства между сотрудниками Гринатома'
                                              ' и стихиями: один с огнем в глазах берется за новые проекты; другой '
                                              'креативный и легкий на подъем как воздушные потоки; есть люди, которых'
                                              ' не остановить в рабочем процессе как бурную реку; а есть люди-титаны,'
                                              ' спокойные и уравновешенные при любых кризисах как скалы. И именно эта '
                                              'уникальность нас всех объединяет.\n'
                                              '\n'
                                              'Самое время получить уникальные навыки: прокачать в себе все стихии и '
                                              'продлить летние энергичные деньки.\n'
                                              '\n'
                                              'Справа снизу есть кнопка, которая откроет меню, нажми её!_\n',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
        else:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, '_Мне нужен только твой_ *номер телефона*\n'
                             , parse_mode="Markdown")
            bot.register_next_step_handler(message, name)
    except Exception as error:
        print(f'start: {error}')
        bot.register_next_step_handler(message, name)


# -------------Пропустить---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'пропустить', content_types=['text'])
def miss(message):
    try:
        bot.send_message(message.chat.id, '_Решил пропустить задание? Ничего страшного, ты можешь пройти его '
                                          'позже, а сейчас выбирай новое!_\n',
                         parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
    except Exception as error:
        print(f'miss: {error}')
        bot.register_next_step_handler(message, miss)


# -------------Огонь 1---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'огонь 1' or message.text.lower() == 'огонь 1 ✅',
                     content_types=['text'])
def fire1_1(message):
    try:
        if check(message.from_user, "fire_1_1"):
            if check(message.from_user, "fire_1_2"):
                bot.send_message(message.chat.id,
                                 '_Вы проходили данный раздел. Выбирайте другой_',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Ох уж эти люди, они так любят прятаться от моего братца Солнышка на своих пляжах. '
                                 'Но кажется эти подают своими зонтиками какие-то сигналы. Что же они говорят?\n'
                                 '\n'
                                 'Ответ напишите в формате: Ответ_\n'
                                 , parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                bot.send_animation(message.chat.id,
                                   'CgACAgIAAxkBAAIBymUBuGq1gX6rUNMxkQ0ur_OhTD9HAAJtNQAC23IQSJkRFhX3xlARMAQ')
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAOEZQF1oHWShV1Rck_ako-srlwsGakAAnfMMRvbcghIdYpfVx2b-iABAAMCAAN5AAMwBA')
                bot.register_next_step_handler(message, fire1_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Огонь 1_',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
            # bot.send_photo(message.chat.id,
            #                'AgACAgIAAxkBAAIBdGQUSliGbcKAQZ5N3Y3fBbdt3WqeAAIQxjEboWegSOJiFHAp2QmyAQADAgADeQADLwQ',)
            bot.register_next_step_handler(message, fire1_2)
    except Exception as error:
        print(f'fire1_1: {error}')
        bot.register_next_step_handler(message, fire1_1)


def fire1_2(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['защита']:
            change(message.from_user, "fire_1_1")
            bot.send_message(message.chat.id,
                             '_Ох уж эти люди, они так любят прятаться от моего братца Солнышка на своих пляжах. '
                             'Но кажется эти подают своими зонтиками какие-то сигналы. Что же они говорят?\n'
                             '\n'
                             'Ответ напишите в формате: Ответ_\n'
                             , parse_mode="Markdown")
            bot.send_animation(message.chat.id,
                               'CgACAgIAAxkBAAP6ZQGC445qkv0soM-YQRWZLmYuS6IAAuQ1AALbcghIP5UtsByzqiUwBA')
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAOEZQF1oHWShV1Rck_ako-srlwsGakAAnfMMRvbcghIdYpfVx2b-iABAAMCAAN5AAMwBA'
                           , reply_markup=keyboard.keyboard_miss())
            bot.register_next_step_handler(message, fire1_3)
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, fire1_2)
    except Exception as error:
        print(f'fire1_2: {error}')
        bot.register_next_step_handler(message, fire1_2)


def fire1_3(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['жарко']:
            if check_final(message.from_user):
                end(message)
            else:
                change(message.from_user, "fire_1_2")
                bot.send_message(message.chat.id,
                                 '_Молодцы. Вы на шаг ближе к освоению очередной ценности_ 👍🏼 _Открывайте меню и '
                                 'поехали дальше!_\n'
                                 , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
                bot.send_message(message.chat.id, "Стикер Огонь 1")
                # bot.send_sticker(message.chat.id,"")
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, fire1_3)
    except Exception as error:
        print(f'fire1_3: {error}')
        bot.register_next_step_handler(message, fire1_3)


# -------------Огонь 2---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'огонь 2' or message.text.lower() == 'огонь 2 ✅',
                     content_types=['text'])
def fire2_1(message):
    try:
        if check(message.from_user, "fire_2_1"):
            if check(message.from_user, "fire_2_2"):
                bot.send_message(message.chat.id,
                                 '_Вы проходили данный раздел. Выбирайте другой_',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Лето самая жаркая пора, так что дам вам свое задание связанное с тем, как вы '
                                 'люди прячетесь от жары. Запираетесь дома, смотрите фильмы под кондиционером. '
                                 'Отгадайте какой я загадал фильм поменяв все слова названия на противоположные_\n'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIBJmUBiugFuCg3G6NpVznbcwjDUffdAALDzDEb23IISJb6zw4DJyZJAQADAgADeQADMAQ'
                               ,reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, fire2_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Огонь 2_',
                             parse_mode="Markdown",reply_markup=keyboard.keyboard_miss())
            # bot.send_photo(message.chat.id,
            #                'AgACAgIAAxkBAAIBdGQUSliGbcKAQZ5N3Y3fBbdt3WqeAAIQxjEboWegSOJiFHAp2QmyAQADAgADeQADLwQ',)
            bot.register_next_step_handler(message, fire2_2)
    except Exception as error:
        print(f'fire2_1: {error}')
        bot.register_next_step_handler(message, fire2_1)


def fire2_2(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['весомость']:
            change(message.from_user, "fire_2_1")
            bot.send_message(message.chat.id,
                             '_Лето самая жаркая пора, так что дам вам свое задание связанное с тем, как вы '
                             'люди прячетесь от жары. Запираетесь дома, смотрите фильмы под кондиционером. '
                             'Отгадайте какой я загадал фильм поменяв все слова названия на противоположные_\n'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIBJmUBiugFuCg3G6NpVznbcwjDUffdAALDzDEb23IISJb6zw4DJyZJAQADAgADeQADMAQ',
                           reply_markup=keyboard.keyboard_miss())
            bot.register_next_step_handler(message, fire2_3)
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, fire2_2)
    except Exception as error:
        print(f'fire2_2: {error}')
        bot.register_next_step_handler(message, fire2_2)


def fire2_3(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['500 дней лета', 'пятьсот дней лета']:
            if check_final(message.from_user):
                end(message)
            else:
                change(message.from_user, "fire_2_2")
                bot.send_message(message.chat.id,
                                 '_Молодцы. Вы на шаг ближе к освоению очередной ценности_ 👍🏼 _Открывайте меню и '
                                 'поехали дальше!_\n'
                                 , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
                bot.send_message(message.chat.id, "Стикер Огонь 2")
                # bot.send_sticker(message.chat.id,"")
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, fire2_3)
    except Exception as error:
        print(f'fire2_3: {error}')
        bot.register_next_step_handler(message, fire2_3)


# -------------Огонь 3---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'огонь 3' or message.text.lower() == 'огонь 3 ✅',
                     content_types=['text'])
def fire3_1(message):
    try:
        if check(message.from_user, "fire_3_1"):
            if check(message.from_user, "fire_3_2"):
                bot.send_message(message.chat.id,
                                 '_Вы проходили данный раздел. Выбирайте другой_',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Настоящие коллеги должны понимать друг друга на любом языке! И даже на языке '
                                 'эмодзи. Попробуйте понять, кто же тут загадан!_\n'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIBJ2UBjOZBmaA8TnO-wj-2ed-clBt5AALRzDEb23IISBUkSaZSFL5DAQADAgADeQADMAQ',
                               reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, fire3_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Огонь 3_',
                             parse_mode="Markdown",reply_markup=keyboard.keyboard_miss())
            # bot.send_photo(message.chat.id,
            #                'AgACAgIAAxkBAAIBdGQUSliGbcKAQZ5N3Y3fBbdt3WqeAAIQxjEboWegSOJiFHAp2QmyAQADAgADeQADLwQ',)
            bot.register_next_step_handler(message, fire3_2)
    except Exception as error:
        print(f'fire3_1: {error}')
        bot.register_next_step_handler(message, fire3_1)


def fire3_2(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['руководитель']:
            change(message.from_user, "fire_3_1")
            bot.send_message(message.chat.id,
                             '_Лето самая жаркая пора, так что дам вам свое задание связанное с тем, как вы '
                             'люди прячетесь от жары. Запираетесь дома, смотрите фильмы под кондиционером. '
                             'Отгадайте какой я загадал фильм поменяв все слова названия на противоположные_\n'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIBJ2UBjOZBmaA8TnO-wj-2ed-clBt5AALRzDEb23IISBUkSaZSFL5DAQADAgADeQADMAQ',
                           reply_markup=keyboard.keyboard_miss())
            bot.register_next_step_handler(message, fire3_3)
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, fire3_2)
    except Exception as error:
        print(f'fire3_2: {error}')
        bot.register_next_step_handler(message, fire3_2)


def fire3_3(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['курчатов']:
            if check_final(message.from_user):
                end(message)
            else:
                change(message.from_user, "fire_3_2")
                bot.send_message(message.chat.id,
                                 '_Молодцы. Вы на шаг ближе к освоению очередной ценности_  👍🏼 _Открывайте меню и '
                                 'поехали дальше!_\n'
                                 , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
                bot.send_message(message.chat.id, "Стикер Огонь 3")
                # bot.send_sticker(message.chat.id,"")
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, fire3_3)
    except Exception as error:
        print(f'fire3_3: {error}')
        bot.register_next_step_handler(message, fire3_3)


# -------------Воздух 1---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'воздух 1' or message.text.lower() == 'воздух 1 ✅',
                     content_types=['text'])
def air1_1(message):
    try:
        if check(message.from_user, "air_1_1"):
            if check(message.from_user, "air_1_2"):
                bot.send_message(message.chat.id,
                                 '_Вы проходили данный раздел. Выбирайте другой_',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Слышите? Ветер доносит ноты очень знакомой песни из пляжного ресторанчика\! '
                                 'Но что же это за песня?_\n'
                                 '\n'
                                 '_Ответ пишите в формате: *Исполнитель\_Название*_'
                                 , parse_mode="MarkdownV2")
                bot.send_audio(message.chat.id,
                               'CQACAgIAAxkBAAIBKGUBkWuoA1DST-Qzl3RIEpjXTA1qAAJaNgAC23IISBbbTcH2f-itMAQ',
                               reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, air1_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Воздух 1_',
                             parse_mode="Markdown",reply_markup=keyboard.keyboard_miss())
            # bot.send_photo(message.chat.id,
            #                'AgACAgIAAxkBAAIBdGQUSliGbcKAQZ5N3Y3fBbdt3WqeAAIQxjEboWegSOJiFHAp2QmyAQADAgADeQADLwQ',)
            bot.register_next_step_handler(message, air1_2)
    except Exception as error:
        print(f'air1_1: {error}')
        bot.register_next_step_handler(message, air1_1)


def air1_2(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['совесть']:
            change(message.from_user, "air_1_1")
            bot.send_message(message.chat.id,
                             '_Слышите? Ветер доносит ноты очень знакомой песни из пляжного ресторанчика! '
                             'Но что же это за песня?_\n'
                             '\n'
                             '_Ответ пишите в формате: ```Исполнитель\\_Название```_'
                             , parse_mode="Markdown")
            bot.send_audio(message.chat.id,
                           'CQACAgIAAxkBAAIBKGUBkWuoA1DST-Qzl3RIEpjXTA1qAAJaNgAC23IISBbbTcH2f-itMAQ',reply_markup=keyboard.keyboard_miss())
            bot.register_next_step_handler(message, air1_3)
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, air1_2)
    except Exception as error:
        print(f'air1_2: {error}')
        bot.register_next_step_handler(message, air1_2)


def air1_3(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ["жанна фриске_где-то лето", "жанна фриске_где то лето", "фриске_лето"
            , "фриске_где то лето", "фриске_где-то лето", "жанна фриске лето", "жанна фриске_лето"]:
            if check_final(message.from_user):
                end(message)
            else:
                change(message.from_user, "air_1_2")
                bot.send_message(message.chat.id,
                                 '_Молодцы. Вы на шаг ближе к освоению очередной ценности_  👍🏼 _Открывайте меню и '
                                 'поехали дальше!_\n'
                                 , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
                bot.send_message(message.chat.id, "Стикер Воздух 1")
                # bot.send_sticker(message.chat.id,"")
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, air1_3)
    except Exception as error:
        print(f'air1_3: {error}')
        bot.register_next_step_handler(message, air1_3)


# -------------Воздух 2---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'воздух 2' or message.text.lower() == 'воздух 2 ✅',
                     content_types=['text'])
def air2_1(message):
    try:
        if check(message.from_user, "air_2_1"):
            if check(message.from_user, "air_2_2"):
                bot.send_message(message.chat.id,
                                 '_Вы проходили данный раздел. Выбирайте другой_',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Вспоминать о лете мы будем еще долго, но чтобы его запомнить еще лучше и '
                                 'детальнее память нужно тренировать! Сможете вспомнить, что же спрятано на картинке?_\n'
                                 '\n'
                                 '_Ответ пишите в формате: Ответ_'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIBKWUBlDwcYdUovnrlFX9kTANsuOkaAALzzDEb23IISMu7e96jWgpQAQADAgADeQADMAQ'
                               ,reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, air2_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Воздух 2_',
                             parse_mode="Markdown",reply_markup=keyboard.keyboard_miss())
            # bot.send_photo(message.chat.id,
            #                'AgACAgIAAxkBAAIBdGQUSliGbcKAQZ5N3Y3fBbdt3WqeAAIQxjEboWegSOJiFHAp2QmyAQADAgADeQADLwQ',)
            bot.register_next_step_handler(message, air2_2)
    except Exception as error:
        print(f'air2_1: {error}')
        bot.register_next_step_handler(message, air2_1)


def air2_2(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['признание']:
            change(message.from_user, "air_2_1")
            bot.send_message(message.chat.id,
                             '_Вспоминать о лете мы будем еще долго, но чтобы его запомнить еще лучше и '
                             'детальнее память нужно тренировать! Сможете вспомнить, что же спрятано на картинке?_\n'
                             '\n'
                             '_Ответ пишите в формате: Ответ_'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIBKWUBlDwcYdUovnrlFX9kTANsuOkaAALzzDEb23IISMu7e96jWgpQAQADAgADeQADMAQ',
                           reply_markup=keyboard.keyboard_miss())
            bot.register_next_step_handler(message, air2_3)
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, air2_2)
    except Exception as error:
        print(f'air2_2: {error}')
        bot.register_next_step_handler(message, air2_2)


def air2_3(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ["памятник", "памятник славскому", "славский"]:
            if check_final(message.from_user):
                end(message)
            else:
                change(message.from_user, "air_2_2")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIBKmUBlUs-i1Gvx_tLykL6AYYDSYHYAAIGzTEb23IISCjL08JPBWSGAQADAgADeQADMAQ')
                bot.send_message(message.chat.id,
                                 '_Молодцы. Вы на шаг ближе к освоению очередной ценности_  👍🏼 _Открывайте меню и '
                                 'поехали дальше!_\n'
                                 , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
                bot.send_message(message.chat.id, "Стикер Воздух 2")
                # bot.send_sticker(message.chat.id,"")
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, air2_3)
    except Exception as error:
        print(f'air2_3: {error}')
        bot.register_next_step_handler(message, air2_3)


# -------------Земля 1---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'земля 1' or message.text.lower() == 'земля 1 ✅',
                     content_types=['text'])
def earth1_1(message):
    try:
        if check(message.from_user, "earth_1_1"):
            if check(message.from_user, "earth_1_2"):
                bot.send_message(message.chat.id,
                                 '_Вы проходили данный раздел. Выбирайте другой_',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Представьте, что вы на пляже потеряли телефон или брошку и теперь вам нужно '
                                 'по своим следам выявить место потери. Для удобства, мы поделили пляж на сектора. '
                                 'Решив эту загадку, никакие потери не будут вам страшны!_\n'
                                 '\n'
                                 '_Ответ пишите в формате: Ответ_'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIBK2UBmu2ynsok1MeDGyX-dIfABcAQAAIC0jEb23IQSN71hr0nhKHHAQADAgADeQADMAQ',
                               reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, earth1_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Земля 1_',
                             parse_mode="Markdown",reply_markup=keyboard.keyboard_miss())
            # bot.send_photo(message.chat.id,
            #                'AgACAgIAAxkBAAIBdGQUSliGbcKAQZ5N3Y3fBbdt3WqeAAIQxjEboWegSOJiFHAp2QmyAQADAgADeQADLwQ',)
            bot.register_next_step_handler(message, earth1_2)
    except Exception as error:
        print(f'earth1_1: {error}')
        bot.register_next_step_handler(message, earth1_1)


def earth1_2(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['время']:
            change(message.from_user, "earth_1_1")
            bot.send_message(message.chat.id,
                             '_Представьте, что вы на пляже потеряли телефон или брошку и теперь вам нужно '
                             'по своим следам выявить место потери. Для удобства, мы поделили пляж на сектора. '
                             'Решив эту загадку, никакие потери не будут вам страшны!_\n'
                             '\n'
                             '_Ответ пишите в формате: Ответ_'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIBK2UBmu2ynsok1MeDGyX-dIfABcAQAAIC0jEb23IQSN71hr0nhKHHAQADAgADeQADMAQ',
                           reply_markup=keyboard.keyboard_miss())
            bot.register_next_step_handler(message, earth1_3)
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, earth1_2)
    except Exception as error:
        print(f'earth1_2: {error}')
        bot.register_next_step_handler(message, earth1_2)


def earth1_3(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ["гимн"]:
            if check_final(message.from_user):
                end(message)
            else:
                change(message.from_user, "earth_1_2")
                bot.send_message(message.chat.id,
                                 '_Молодцы. Вы на шаг ближе к освоению очередной ценности_  👍🏼 _Открывайте меню и '
                                 'поехали дальше!_\n'
                                 , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
                bot.send_message(message.chat.id, "Стикер Земля 1")
                # bot.send_sticker(message.chat.id,"")
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, earth1_3)
    except Exception as error:
        print(f'earth1_3: {error}')
        bot.register_next_step_handler(message, earth1_3)


# -------------Земля 2---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'земля 2' or message.text.lower() == 'земля 2 ✅',
                     content_types=['text'])
def earth2_1(message):
    try:
        if check(message.from_user, "earth_2_1"):
            if check(message.from_user, "earth_2_2"):
                bot.send_message(message.chat.id,
                                 '_Вы проходили данный раздел. Выбирайте другой_',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Нейросети сейчас окружают нас даже в путешествиях, помогая составить маршруты'
                                 ' или рассказывая и показывая красивые места.\n'
                                 'Здесь нейросеть попросили показать известное крылатое выражение, которое связано '
                                 'с путешествиями. Напишите какое._\n'
                                 '\n'
                                 '_Ответ присылайте в формате: Крылатое выражение _'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIBLGUBnQOOGLmDoOyoAfquJBPHzc8HAAIz0jEb23IQSFCr9Se3d6WHAQADAgADeQADMAQ'
                               ,reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, earth2_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Земля 2_',
                             parse_mode="Markdown",reply_markup=keyboard.keyboard_miss())
            # bot.send_photo(message.chat.id,
            #                'AgACAgIAAxkBAAIBdGQUSliGbcKAQZ5N3Y3fBbdt3WqeAAIQxjEboWegSOJiFHAp2QmyAQADAgADeQADLwQ',)
            bot.register_next_step_handler(message, earth2_2)
    except Exception as error:
        print(f'earth2_1: {error}')
        bot.register_next_step_handler(message, earth2_1)


def earth2_2(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['время']:
            change(message.from_user, "earth_2_1")
            bot.send_message(message.chat.id,
                             '_Нейросети сейчас окружают нас даже в путешествиях, помогая составить маршруты'
                             ' или рассказывая и показывая красивые места.\n'
                             'Здесь нейросеть попросили показать известное крылатое выражение, которое связано '
                             'с путешествиями. Напишите какое._\n'
                             '\n'
                             '_Ответ присылайте в формате: Крылатое выражение _'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIBLGUBnQOOGLmDoOyoAfquJBPHzc8HAAIz0jEb23IQSFCr9Se3d6WHAQADAgADeQADMAQ',
                           reply_markup=keyboard.keyboard_miss())
            bot.register_next_step_handler(message, earth2_3)
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, earth2_2)
    except Exception as error:
        print(f'earth2_2: {error}')
        bot.register_next_step_handler(message, earth2_2)


def earth2_3(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ["гимн"]:
            if check_final(message.from_user):
                end(message)
            else:
                change(message.from_user, "earth_2_2")
                bot.send_message(message.chat.id,
                                 '_Молодцы. Вы на шаг ближе к освоению очередной ценности_  👍🏼 _Открывайте меню и '
                                 'поехали дальше!_\n'
                                 , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
                bot.send_message(message.chat.id, "Стикер Земля 2")
                # bot.send_sticker(message.chat.id,"")
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, earth2_3)
    except Exception as error:
        print(f'earth2_3: {error}')
        bot.register_next_step_handler(message, earth2_3)


# -------------Земля 3 (на доработке)---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'земля 3' or message.text.lower() == 'земля 3 ✅',
                     content_types=['text'])
def earth3_1(message):
    try:
        if check(message.from_user, "earth_3_1"):
            if check(message.from_user, "earth_3_2"):
                bot.send_message(message.chat.id,
                                 '_Вы проходили данный раздел. Выбирайте другой_',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Вы давно ходили в поход? Или вообще не ходили? Ничего страшного, сейчас вместе'
                                 ' к нему подготовимся. Нас ждет путешествие по горам Кавказа, 2 ночи у озера, жаркая,'
                                 ' но дождливая погода, так что возьмите с собой все, что может для этого пригодиться.'
                                 ' Ниже в стикерах можете выбрать вещи которые вам понадобиться, четырех будет '
                                 'достаточно, остальное уже собрано._'
                                 , parse_mode="Markdown")
                bot.send_sticker(message.chat.id,
                               'CAACAgIAAxkBAAEKSrdlAievMcMK_16ed7RacF0pzcFZiwACvzUAAhu2-UvUOmjztTLceDAE'
                               ,reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, earth3_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Земля 3_',
                             parse_mode="Markdown",reply_markup=keyboard.keyboard_miss())
            # bot.send_photo(message.chat.id,
            #                'AgACAgIAAxkBAAIBdGQUSliGbcKAQZ5N3Y3fBbdt3WqeAAIQxjEboWegSOJiFHAp2QmyAQADAgADeQADLwQ',)
            bot.register_next_step_handler(message, earth3_2)
    except Exception as error:
        print(f'earth3_1: {error}')
        bot.register_next_step_handler(message, earth3_1)


def earth3_2(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['тимбилдинг']:
            change(message.from_user, "earth_3_1")
            bot.send_message(message.chat.id,
                             '_Вы давно ходили в поход? Или вообще не ходили? Ничего страшного, сейчас вместе'
                             ' к нему подготовимся. Нас ждет путешествие по горам Кавказа, 2 ночи у озера, жаркая,'
                             ' но дождливая погода, так что возьмите с собой все, что может для этого пригодиться.'
                             ' Ниже в стикерах можете выбрать вещи которые вам понадобиться, четырех будет '
                             'достаточно, остальное уже собрано._'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIBLGUBnQOOGLmDoOyoAfquJBPHzc8HAAIz0jEb23IQSFCr9Se3d6WHAQADAgADeQADMAQ',
                           reply_markup=keyboard.keyboard_miss())
            bot.register_next_step_handler(message, earth3_3)
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, earth3_2)
    except Exception as error:
        print(f'earth3_2: {error}')
        bot.register_next_step_handler(message, earth3_2)


def earth3_3(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ["гимн"]:
            if check_final(message.from_user):
                end(message)
            else:
                change(message.from_user, "earth_3_2")
                bot.send_message(message.chat.id,
                                 '_Молодцы. Вы на шаг ближе к освоению очередной ценности_  👍🏼 _Открывайте меню и '
                                 'поехали дальше!_\n'
                                 , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
                bot.send_message(message.chat.id, "Стикер Земля 3")
                # bot.send_sticker(message.chat.id,"")
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, earth3_3)
    except Exception as error:
        print(f'earth3_3: {error}')
        bot.register_next_step_handler(message, earth3_3)


# -------------Вода 1---------------------------
@bot.message_handler(func=lambda message: message.text.lower() == 'вода 1' or message.text.lower() == 'вода 1 ✅',
                     content_types=['text'])
def water1_1(message):
    try:
        if check(message.from_user, "water_1_1"):
            if check(message.from_user, "water_1_2"):
                bot.send_message(message.chat.id,
                                 '_Вы проходили данный раздел. Выбирайте другой_',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Представьте, что вы попали в гости к своему другу, который только вернулся '
                                 'из отпуска. Вы очень хотите его удивить, рассказав о его отпуске вместо него. '
                                 'Для этого вам понадобится внимательность, ведь он еще не успел разобрать вещи. '
                                 'Посмотрите внимательно на комнату и попробуйте догадаться где был ваш друг._\n'
                                 '\n'
                                 '_Ответ присылайте в формате: слово. В одном сообщении ответ на один вопрос._'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIBLWUBoJC3KwbXehKn7SuoDNrKrPe0AAJC0jEb23IQSCt3cz2nSAABDwEAAwIAA3kAAzAE')
                bot.send_document(message.chat.id,
                                  'BQACAgIAAxkBAAIBLmUBoTsZsWP2hMxHHI1wktzH2S8NAAJpNAAC23IQSHT41Md5G-AIMAQ',
                                  reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, water1_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Вода 1_',
                             parse_mode="Markdown",
                             reply_markup=keyboard.keyboard_miss())
            # bot.send_photo(message.chat.id,
            #                'AgACAgIAAxkBAAIBdGQUSliGbcKAQZ5N3Y3fBbdt3WqeAAIQxjEboWegSOJiFHAp2QmyAQADAgADeQADLwQ',)
            bot.register_next_step_handler(message, water1_2)
    except Exception as error:
        print(f'water1_1: {error}')
        bot.register_next_step_handler(message, water1_1)


def water1_2(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['время']:
            change(message.from_user, "water_1_1")
            bot.send_message(message.chat.id,
                             '_Представьте, что вы попали в гости к своему другу, который только вернулся '
                             'из отпуска. Вы очень хотите его удивить, рассказав о его отпуске вместо него. '
                             'Для этого вам понадобится внимательность, ведь он еще не успел разобрать вещи. '
                             'Посмотрите внимательно на комнату и попробуйте догадаться где был ваш друг._\n'
                             '\n'
                             '_Ответ присылайте в формате: слово. В одном сообщении ответ на один вопрос._'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIBLWUBoJC3KwbXehKn7SuoDNrKrPe0AAJC0jEb23IQSCt3cz2nSAABDwEAAwIAA3kAAzAE')
            bot.send_document(message.chat.id,
                              'BQACAgIAAxkBAAIBLmUBoTsZsWP2hMxHHI1wktzH2S8NAAJpNAAC23IQSHT41Md5G-AIMAQ',
                              reply_markup=keyboard.keyboard_miss())
            bot.register_next_step_handler(message, water1_3)
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, water1_2)
    except Exception as error:
        print(f'water1_2: {error}')
        bot.register_next_step_handler(message, water1_2)


def water1_3(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        if message.text.lower() in ['cочи']:
            if check_answer(message.chat, 'answer', "answer_1"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown",reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, water1_3)
            else:
                bot.send_message(message.chat.id,
                                 'Прекрасно справляешься!',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                change_answer(message.chat, 'answer', "answer_1")
                if check_answer_final(message.chat, 'answer'):
                    final_water1_3(message)
                else:
                    bot.register_next_step_handler(message, water1_3)
        elif message.text.lower() in ['сувенир', 'сувенирную тарелку', 'тарелку', 'тарелка', 'сувенирная тарелка']:
            if check_answer(message.chat, 'answer', "answer_2"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, water1_3)
            else:
                bot.send_message(message.chat.id,
                                 'Прекрасно справляешься!',
                                 parse_mode="Markdown",reply_markup=keyboard.keyboard_miss() )
                change_answer(message.chat, 'answer', "answer_2")
                if check_answer_final(message.chat, 'answer'):
                    final_water1_3(message)
                else:
                    bot.register_next_step_handler(message, water1_3)
        elif message.text.lower() in ['самолёт', 'на самолёте', 'самолётом', 'самолет', 'на самолете', 'самолетом']:
            if check_answer(message.chat, 'answer', "answer_3"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown",reply_markup=keyboard.keyboard_miss() )
                bot.register_next_step_handler(message, water1_3)
            else:
                bot.send_message(message.chat.id,
                                 'Прекрасно справляешься!',
                                 parse_mode="Markdown",reply_markup=keyboard.keyboard_miss() )
                change_answer(message.chat, 'answer', "answer_3")
                if check_answer_final(message.chat, 'answer'):
                    final_water1_3(message)
                else:
                    bot.register_next_step_handler(message, water1_3)
        elif message.text.lower() in ['сёрфинг', 'сёрфингом', 'серфинг', 'серфингом']:
            if check_answer(message.chat, 'answer', "answer_4"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, water1_3)
            else:
                bot.send_message(message.chat.id,
                                 'Прекрасно справляешься!',
                                 parse_mode="Markdown",reply_markup=keyboard.keyboard_miss() )
                change_answer(message.chat, 'answer', "answer_4")
                if check_answer_final(message.chat, 'answer'):
                    final_water1_3(message)
                else:
                    bot.register_next_step_handler(message, water1_3)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, water1_3)

    except Exception as error:
        print(f'water1_3: {error}')
        bot.register_next_step_handler(message, water1_3)


def final_water1_3(message):
    change(message.from_user, "water_1_2")
    bot.send_message(message.chat.id,
                     '_Молодцы. Вы на шаг ближе к освоению очередной ценности_ 👍🏼 '
                     '_Открывайте меню и поехали дальше!_', parse_mode="Markdown",
                     reply_markup=keyboard.keyboard(message.from_user))
    bot.send_message(message.chat.id, "Стикер Вода 1")
    # bot.send_sticker(message.chat.id,"")


# -------------Вода 2---------------------------
photo = [
    'AgACAgIAAxkBAAIBL2UBp4PVb0RnPemQeAAB0AQ_01_b0QACatIxG9tyEEiFzGMpDpplIQEAAwIAA3kAAzAE',
    'AgACAgIAAxkBAAIBMGUBp5qV6-B9b8JsgguVrPx4v4RKAAJr0jEb23IQSLwWt8P8s2LQAQADAgADeQADMAQ',
    'AgACAgIAAxkBAAIBMWUBp7SbEFy-jwi70_gaoqGzrQk9AAJu0jEb23IQSIh00uzci50-AQADAgADeQADMAQ',
    'AgACAgIAAxkBAAIBMmUBp8xuOKETJHaR9VM8KRwRfQS5AAJv0jEb23IQSOO9DPyZE_33AQADAgADeQADMAQ'
]


@bot.message_handler(func=lambda message: message.text.lower() == 'вода 2' or message.text.lower() == 'вода 2 ✅',
                     content_types=['text'])
def water2_1(message):
    try:
        if check(message.from_user, "water_2_1"):
            if check(message.from_user, "water_2_2"):
                bot.send_message(message.chat.id,
                                 '_Вы проходили данный раздел. Выбирайте другой_',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Обожаю когда ко мне летом приезжает много людей, играют со мной и '
                                 'фотографируются на память. Хочу и сейчас чтобы вы оставили мне свои фотокарточки '
                                 'на память, держите пример, сделайте похожее фото и пришлите сюда._\n',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                bot.send_photo(message.chat.id,
                               random.choice(photo))
                bot.register_next_step_handler(message, water2_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Вода 2_',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
            # bot.send_photo(message.chat.id,
            #                'AgACAgIAAxkBAAIBdGQUSliGbcKAQZ5N3Y3fBbdt3WqeAAIQxjEboWegSOJiFHAp2QmyAQADAgADeQADLwQ',)
            bot.register_next_step_handler(message, water2_2)
    except Exception as error:
        print(f'water2_1: {error}')
        bot.register_next_step_handler(message, water2_1)


def water2_2(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        elif message.text.lower() in ['группа']:
            change(message.from_user, "water_2_1")
            bot.send_message(message.chat.id,
                             '_Обожаю когда ко мне летом приезжает много людей, играют со мной и '
                             'фотографируются на память. Хочу и сейчас чтобы вы оставили мне свои фотокарточки '
                             'на память, держите пример, сделайте похожее фото и пришлите сюда._\n',
                             parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           random.choice(photo), reply_markup=keyboard.keyboard_miss())
            bot.register_next_step_handler(message, water2_3)
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, water2_2)
    except Exception as error:
        print(f'water2_2: {error}')
        bot.register_next_step_handler(message, water2_2)


def water2_3(message):
    try:
        if message.text.lower() in ['пропустить']:
            miss(message)
        if message.content_type == 'photo':
            keyboard_inline = types.InlineKeyboardMarkup()
            confirm_button = types.InlineKeyboardButton('Подтвердить', callback_data='confirm')
            cancel_button = types.InlineKeyboardButton('Отменить', callback_data='cancel')
            keyboard_inline.row(confirm_button, cancel_button)
            bot.send_photo(admin_id, message.photo[-1].file_id,
                           caption=f'Подтвердите отправку этой фотографии для "{message.from_user.first_name}":\n'
                                   f'\n'
                                   f'Задание Вода 2:\n'
                                   f'\n'
                                   f'[ {message.chat} ]'
                                   f'#question_4#',
                           reply_markup=keyboard_inline)

            @bot.callback_query_handler(func=lambda call: True)
            def callback_handler(call):
                text = call.message.caption
                match = re.search(r'\[(.*?)\]', text)
                question = re.search(r'\#(.*?)\#', text)
                text = match.group(1).replace("'", "\"")
                text_end = text.replace("None", "null")
                value = json.loads(text_end)
                chat = types.Chat.de_json(value)
                if call.data == 'confirm':
                    bot.send_message(call.from_user.id, f'Фотография подтверждена у \"{message.from_user.first_name}\"')
                    # bot.delete_message(call.from_user.id, call.message.id)
                    change(message.from_user, "water_2_2")
                    bot.send_message(chat.id,
                                     '_Молодцы. Вы на шаг ближе к освоению очередной ценности_ 👍🏼 _Открывай меню, '
                                     'поехали дальше_',parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
                    if check_final(chat):
                        end(message)
                elif call.data == 'cancel':
                    bot.send_message(chat.id, 'Хм.. даю ещё шанс 😊')
                    # bot.delete_message(call.from_user.id, call.message.id)
                    bot.send_message(call.from_user.id, f'Фотография отменена у \"{message.from_user.first_name}\"')
                    bot.register_next_step_handler(message, water2_3)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, 'Нужно фото\n',
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, water2_3)
    except Exception as error:
        print(f'water2_3: {error}')
        bot.register_next_step_handler(message, water2_3)


def end(message):
    bot.send_sticker(message.chat.id,
                     "CAACAgIAAxkBAAEIHzFkDzxFeaWhNjihFqQaSFaZNWMzSAACWyoAAvMreEibkHdAfD2kCS8E")
    bot.send_message(message.chat.id, '_Вау! Я в восторге от того, как хорошо ты разбираешься в ценностях компании.'
                                      ' Я тобой горжусь. Потому что самая главная, СЕКРЕТНАЯ, ценность нашей '
                                      'компании – её люди. Это ТЫ!\n'
                                      '\n'
                                      'Впереди ещё очень много интересного. Желаю тебе приятного отдыха на пляже '
                                      '“Улетай”_\n',
                     parse_mode="Markdown", disable_web_page_preview=True)
    bot.register_next_step_handler(message, end)


def change(user_data, name_colum):
    database = db.Data(user_data)
    database.replace(name_colum)


def change_answer(user_data, table_name, name_colum):
    database = db.Data(user_data)
    database.replace_answer(table_name, name_colum)


def check(user_id, name_colum):
    database = db.Data(user_id)
    number = database.check(name_colum)
    return number


def check_final(user_data):
    database = db.Data(user_data)
    number = database.check_final()
    if all(number):
        database.final()
        return True
    else:
        return False


def check_answer_final(user_data, table_name):
    database = db.Data(user_data)
    number = database.check_answer_final(table_name)
    if all(number):
        return True
    else:
        return False


def check_answer(user_data, table_name, name_colum):
    database = db.Data(user_data)
    answer_bool = database.response_answer(table_name, name_colum)
    if answer_bool[0]:
        return True
    else:
        return False


def collector(message):
    user = db.Data(message.from_user)
    if bool(message.from_user.username) is True:
        name = message.text
        username = f'https://t.me/{message.from_user.username}'
        user.collection(name, username)
    else:
        name = message.text
        user.collection(name)


def set_surname(message):
    user = db.Data(message.from_user)
    surname = message.text
    user.setSurname(surname)


def set_name(message):
    user = db.Data(message.from_user)
    name = message.text
    user.setName(name)


def set_phone(message):
    user = db.Data(message.from_user)
    phone = message.text
    user.setPhone(phone)


while True:
    try:
        bot.polling(none_stop=True, timeout=10)
    except Exception as error:
        print(error)
        time.sleep(3)
