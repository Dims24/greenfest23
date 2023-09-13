import random
import telebot
from datetime import datetime
import time
import os
from telebot.types import InputFile

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
menedjer = 483241197
menedjer_1 = 703608663


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
            setSurname(message)
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
            setName(message)
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
            setPhone(message)
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
                                 parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Ох уж эти люди, они так любят прятаться от моего братца Солнышка на своих пляжах. '
                                 'Но кажется эти подают своими зонтиками какие-то сигналы. Что же они говорят?\n'
                                 '\n'
                                 'Ответ напишите в формате: Ответ_\n'
                                 , parse_mode="Markdown")
                bot.send_animation(message.chat.id,
                                   'AAMCAgADGQEAA4NlAXVjaamg6iMcZJ2F5junybau2gACijUAAttyCEirQ648afbeKgEAB20AAzAE')
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAOEZQF1oHWShV1Rck_ako-srlwsGakAAnfMMRvbcghIdYpfVx2b-iABAAMCAAN5AAMwBA')
                bot.register_next_step_handler(message, fire1_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Огонь 1_',
                             parse_mode="Markdown")
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
                           'AgACAgIAAxkBAAOEZQF1oHWShV1Rck_ako-srlwsGakAAnfMMRvbcghIdYpfVx2b-iABAAMCAAN5AAMwBA')
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
                                 parse_mode="Markdown")
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
                               'AgACAgIAAxkBAAIBJmUBiugFuCg3G6NpVznbcwjDUffdAALDzDEb23IISJb6zw4DJyZJAQADAgADeQADMAQ')
                bot.register_next_step_handler(message, fire2_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Огонь 2_',
                             parse_mode="Markdown")
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
                           'AgACAgIAAxkBAAIBJmUBiugFuCg3G6NpVznbcwjDUffdAALDzDEb23IISJb6zw4DJyZJAQADAgADeQADMAQ')
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
                                 parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Настоящие коллеги должны понимать друг друга на любом языке! И даже на языке '
                                 'эмодзи. Попробуйте понять, кто же тут загадан!_\n'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAAIBJ2UBjOZBmaA8TnO-wj-2ed-clBt5AALRzDEb23IISBUkSaZSFL5DAQADAgADeQADMAQ')
                bot.register_next_step_handler(message, fire3_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Огонь 3_',
                             parse_mode="Markdown")
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
                             'Отгадайте какой я загадал фильм поменяв все слова названия на противоположные\n'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIBJ2UBjOZBmaA8TnO-wj-2ed-clBt5AALRzDEb23IISBUkSaZSFL5DAQADAgADeQADMAQ')
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
                                 parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id,
                                 '_Вы проходили данное задание. Переходим к этапу 2_',
                                 parse_mode="Markdown")
                bot.send_message(message.chat.id,
                                 '_Слышите? Ветер доносит ноты очень знакомой песни из пляжного ресторанчика! '
                                 'Но что же это за песня?_\n'
                                 '\n'
                                 '_Ответ пишите в формате: Исполнитель_Название_'
                                 , parse_mode="Markdown")
                bot.send_audio(message.chat.id,
                               'CQACAgIAAxkBAAIBKGUBkWuoA1DST-Qzl3RIEpjXTA1qAAJaNgAC23IISBbbTcH2f-itMAQ')
                bot.register_next_step_handler(message, air1_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Воздух 1_',
                             parse_mode="Markdown")
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
                             '_Ответ пишите в формате: Исполнитель_Название_'
                             , parse_mode="Markdown")
            bot.send_audio(message.chat.id,
                           'CQACAgIAAxkBAAIBKGUBkWuoA1DST-Qzl3RIEpjXTA1qAAJaNgAC23IISBbbTcH2f-itMAQ')
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
                                 parse_mode="Markdown")
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
                               'AgACAgIAAxkBAAIBKWUBlDwcYdUovnrlFX9kTANsuOkaAALzzDEb23IISMu7e96jWgpQAQADAgADeQADMAQ')
                bot.register_next_step_handler(message, air2_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Воздух 2_',
                             parse_mode="Markdown")
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
                           'AgACAgIAAxkBAAIBKWUBlDwcYdUovnrlFX9kTANsuOkaAALzzDEb23IISMu7e96jWgpQAQADAgADeQADMAQ')
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


def antiquiz_two(message):
    try:
        if message.text.lower() in ['охотники за привидениями']:
            bot.send_message(message.chat.id,
                             'Отличная работа!'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIBzWQUVjzao6LFm5nwcv5Cv29JnLJRAAJoxjEboWegSFKMdChU_tgZAQADAgADeQADLwQ',
                           )
            bot.register_next_step_handler(message, antiquiz_three)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, antiquiz_two)
    except Exception as error:
        print(f'antiquiz: {error}')
        bot.register_next_step_handler(message, antiquiz_two)


def antiquiz_three(message):
    try:
        if message.text.lower() in ['титаник']:
            bot.send_message(message.chat.id,
                             'Отличная работа!'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIBzmQUV7-hypf9o0xw3rt4fScBm2lSAAJwxjEboWegSJekAAGDl-DLcQEAAwIAA3kAAy8E',
                           )
            bot.register_next_step_handler(message, antiquiz_end)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, antiquiz_three)
    except Exception as error:
        print(f'antiquiz_three: {error}')
        bot.register_next_step_handler(message, antiquiz_three)


def antiquiz_end(message):
    try:
        if message.text.lower() in ['шерлок',
                                    'шерлок холмс',
                                    'шерлок ббс',
                                    'шерлок bbc',
                                    'sherlock bbc',
                                    'шерлок холмс и доктор ватсон']:
            change(message.from_user, "antiquiz")
            if check_final(message.from_user):
                end(message)
            else:
                bot.send_message(message.chat.id,
                                 'Отличная работа!',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
                bot.send_message(message.chat.id,
                                 '*Telegram-игры* – это:\n'
                                 '\n'
                                 '🔸 Новый формат корпоративных игр: не похож на классические предложения '
                                 '(онлайн-импровизации, онлайн ролевые игры, онлайн-мастер-классы и тп)\n'
                                 '🔸 Игра-конструктор: можем выбрать сложность игры, длительность, тематику, '
                                 'задания, и другие доп.функции\n'
                                 '🔸 Технологичность: проведение игр с помощью Telegram-бота\n'
                                 '🔸 Эксклюзивность: каждая игра брендируется под Заказчика\n'
                                 '🔸 Гарантии: тестируем игру с заказчиком за 2-е суток до мероприятия для правок\n'
                                 '🔸 Удалённая организация под ключ: оптимизация времени\n'
                                 '🔸 Неограниченное кол-во участников\n'
                                 '🔸 Индивидуальная или командная игра!\n'
                                 '\n'
                                 'Возвращайся в меню 🥰',
                                 parse_mode="Markdown", reply_markup=keyboard.telegram_quest_inline())
                if check_final(message.from_user):
                    end(message)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, 'Хм.. предлагаю подумать ещё 😊\n',
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, antiquiz_end)
    except Exception as error:
        print(f'antiquiz_end: {error}')
        bot.register_next_step_handler(message, antiquiz_end)


@bot.message_handler(func=lambda message: message.text.lower() == 'шатры' or message.text.lower() == 'шатры ✅',
                     content_types=['text'])
def tents(message):
    try:
        if check(message.from_user, "tents"):
            bot.send_message(message.chat.id,
                             'Вы проходили данное задание',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            bot.send_message(message.chat.id,
                             'Шатры с установкой под ключ – это мастхэв для уличного мероприятия. Готовые шатры красивы, они '
                             'хорошо защищают от погодных проявлений. Они позволят укрыться от дождя, ветра или солнца в '
                             'жаркую погоду. Дополнительно можно смонтировать сцену, арендовать банкетные или фуршетные '
                             'столы и стулья для гостей.\n'
                             '\n'
                             'Про мебель рассказываю отдельно 😏\n'
                             '\n'
                             'Возвращайся в меню 🥰',
                             parse_mode="Markdown", reply_markup=keyboard.telegram_tent_inline())
        else:
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEIHeNkDu9Wd5gvELZtO3MK7S8Y2b8QKgAC5ysAAvIMWEiBgimOerPlQi8E")
            bot.send_message(message.chat.id,
                             '🧩 Ой, шатры – это вообще шикарное круглогодичное решение! У нас они все в '
                             'собственности и готовы в любую погоду и время года служить на вашем ивенте.\n'
                             '\n'
                             'Кстати, о задании: представь, что ты – организатор свадебного торжества и '
                             'прямо сейчас '
                             'завершается монтаж площадки. Нужно внимательно оценить идеальную готовность '
                             'и понять, не осталось ли на площадке что-то лишнее. Потому что всё лишнее,'
                             ' конечно, нужно убрать. \n'
                             'Главное – в н и м а т е л ь н о с т ь. Её-то сейчас и проверим))\n'
                             '\n'
                             '✅ _Назови 4 атрибута, которые *не* потребуются на этом мероприятии. Один '
                             'лишний предмет – один ответ. Давать ответы можно в произвольном порядке._',
                             parse_mode="Markdown")
            bot.send_document(message.chat.id,
                              'BQACAgIAAxkBAAINP2QcYGv1LXmOSrRCHVXPVMYTMLlAAAKJKQACos_pSOplKiW5_zLULwQ')
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAICIGQVhbzCUTCpsr1NwYMAAe9TMChpJgAC38YxG6FnqEi-V1BXqjzYeQEAAwIAA3kAAy8E',
                           )
            bot.register_next_step_handler(message, tents_end)
    except Exception as error:
        print(f'tents: {error}')
        bot.register_next_step_handler(message, tents)


def tents_end(message):
    try:
        # if check_answer_final(message.from_user, 'tent_answer'):
        #     end(message)
        #     change(message.from_user, "tents")
        if message.text.lower() in ['мишка',
                                    'медвежонок',
                                    'медведь',
                                    'плюшевый мишка',
                                    'плюшевый медведь',
                                    'мягкая игрушка',
                                    'игрушка']:
            if check_answer(message.from_user, 'tent_answer', "answer_1"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", )
                bot.register_next_step_handler(message, tents_end)
            else:
                bot.send_message(message.chat.id,
                                 'Прекрасно справляешься!',
                                 parse_mode="Markdown", )
                change_answer(message.from_user, 'tent_answer', "answer_1")
                change_answer(message.from_user, 'tent_answer', "answer_5")
                if check_answer_final(message.from_user, 'tent_answer'):
                    change(message.from_user, "tents")
                    tents_end_message(message)
                else:
                    bot.register_next_step_handler(message, tents_end)
        elif message.text.lower() in ['меню',
                                      'менюшка']:
            if check_answer(message.from_user, 'tent_answer', "answer_2"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", )
                bot.register_next_step_handler(message, tents_end)
            else:
                bot.send_message(message.chat.id,
                                 'Прекрасно справляешься!',
                                 parse_mode="Markdown", )
                change_answer(message.from_user, 'tent_answer', "answer_2")
                change_answer(message.from_user, 'tent_answer', "answer_5")
                if check_answer_final(message.from_user, 'tent_answer'):
                    change(message.from_user, "tents")
                    tents_end_message(message)
                else:
                    bot.register_next_step_handler(message, tents_end)
        elif message.text.lower() in ['ёлка',
                                      'елка',
                                      'новогодняя ёлка',
                                      'новогодняя елка',
                                      'ель']:
            if check_answer(message.from_user, 'tent_answer', "answer_3"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", )
                bot.register_next_step_handler(message, tents_end)
            else:
                bot.send_message(message.chat.id,
                                 'Прекрасно справляешься!',
                                 parse_mode="Markdown", )
                change_answer(message.from_user, 'tent_answer', "answer_3")
                change_answer(message.from_user, 'tent_answer', "answer_5")
                if check_answer_final(message.from_user, 'tent_answer'):
                    change(message.from_user, "tents")
                    tents_end_message(message)
                else:
                    bot.register_next_step_handler(message, tents_end)
        elif message.text.lower() in ['веник',
                                      'веник и совок',
                                      'веник,совок',
                                      'веник с совком',
                                      'совок',
                                      'совок и веник',
                                      'совок с веником',
                                      'швабра',
                                      'швабра с совком',
                                      'совок с шваброй',
                                      'метла',
                                      'метла и совок',
                                      'метла с совком',
                                      'совок с метлой']:
            if check_answer(message.from_user, 'tent_answer', "answer_4"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", )
                bot.register_next_step_handler(message, tents_end)
            else:
                bot.send_message(message.chat.id,
                                 'Прекрасно справляешься!',
                                 parse_mode="Markdown", )
                change_answer(message.from_user, 'tent_answer', "answer_4")
                change_answer(message.from_user, 'tent_answer', "answer_5")
                if check_answer_final(message.from_user, 'tent_answer'):
                    change(message.from_user, "tents")
                    tents_end_message(message)
                else:
                    bot.register_next_step_handler(message, tents_end)
        else:
            bot.send_message(message.chat.id,
                             'Пу-пу-пу.. немного не то😊',
                             parse_mode="Markdown", )
            bot.register_next_step_handler(message, tents_end)
    except Exception as error:
        print(f'tents_end: {error}')
        bot.register_next_step_handler(message, tents_end)


def tents_end_message(message):
    try:
        bot.send_message(message.chat.id,
                         'Отличная работа!',
                         parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
        bot.send_message(message.chat.id,
                         'Шатры с установкой под ключ – это мастхэв для уличного мероприятия. Готовые шатры красивы, они '
                         'хорошо защищают от погодных проявлений. Они позволят укрыться от дождя, ветра или солнца в '
                         'жаркую погоду. Дополнительно можно смонтировать сцену, арендовать банкетные или фуршетные '
                         'столы и стулья для гостей.\n'
                         '\n'
                         'Про мебель рассказываю отдельно 😏\n'
                         '\n'
                         'Возвращайся в меню 🥰',
                         parse_mode="Markdown", reply_markup=keyboard.telegram_tent_inline())
        if check_final(message.from_user):
            end(message)
    except Exception as error:
        print(f'tents_end_message: {error}')
        bot.register_next_step_handler(message, tents_end)

    # bot.register_next_step_handler(message, tents)


@bot.message_handler(func=lambda message: message.text.lower() == 'мебель' or message.text.lower() == 'мебель ✅',
                     content_types=['text'])
def furniture(message):
    try:
        if check(message.from_user, "furniture"):
            bot.send_message(message.chat.id,
                             'Вы проходили данное задание',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            bot.send_message(message.chat.id,
                             'Мероприятие любят не только за его наполнение, но и глазами. Потому, рекомендуем выдерживать '
                             'в любом ивенте общий стиль. Мебель и текстиль, а также интересный декор – это всегда '
                             'прекрасно.\n'
                             '\n'
                             'Возвращайся в меню 🥰',
                             parse_mode="Markdown", reply_markup=keyboard.telegram_furniture_inline())
        else:
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEIHzNkDzxnlVv7wpIeJ4ZD_XT8uzXKAAOpJgACYSKBSOj2j1mbeI4SLwQ")
            bot.send_message(message.chat.id,
                             '🧩 Не существует мероприятий без мебели… ну онлайн разве только 😀 Она везде нужна: пуфики, '
                             'гардероб, зеркало в гримёрку, гамаки на природу, паллетные столы… В общем, если я начну '
                             'перечислять всё, что у нас есть, мы пробудем в этом чате ещё очень-очень долго))\n'
                             '\n'
                             'Предлагаю сразу к заданию! Я превратил 5 предметов мебели в анаграмму. Это когда буквы в '
                             'существующем слове перемешаны.\n'
                             '\n'
                             '✅ _Попробуй понять, какие слова я “зашифровал” и вписать их в кроссворд. Главным ответом на этот '
                             'раунд будет слово из_ *красных* _окошек.\n'
                             '\n'
                             'Каждое слово можно проверить. Пиши мне предполагаемую разгадку в таком формате без '
                             'пробелов_ *1ответ.*\n',
                             parse_mode="Markdown", reply_markup=keyboard.crossworld())
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAICzGQVpBiiHqWXPhItEBIy_t0PisOdAAJxxzEboWeoSKojveZ7k4K5AQADAgADeQADLwQ')
            bot.register_next_step_handler(message, furniture_check)
    except Exception as error:
        print(f'furniture: {error}')
        bot.register_next_step_handler(message, furniture)


def furniture_check(message):
    try:
        if message.text.lower() in ['1кресло']:
            if check_answer(message.from_user, 'furniture_answer', "answer_1"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", )
                bot.register_next_step_handler(message, furniture_check)
            else:
                bot.send_message(message.chat.id,
                                 'Верно',
                                 parse_mode="Markdown", )
                change_answer(message.from_user, 'furniture_answer', "answer_1")
                if check_answer_final(message.from_user, 'furniture_answer'):
                    change(message.from_user, "furniture")
                    bot.send_photo(message.chat.id,
                                   'AgACAgIAAxkBAAICzWQVrj9GWMcYaaYWWXPdN4Kan-OdAAKtxzEboWeoSBaPwuII2i2-AQADAgADeQADLwQ',
                                   reply_markup=keyboard.crossworld())
                    bot.register_next_step_handler(message, furniture_end_message)
                else:
                    bot.register_next_step_handler(message, furniture_check)
        elif message.text.lower() in ['2стул']:
            if check_answer(message.from_user, 'furniture_answer', "answer_2"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", )
                bot.register_next_step_handler(message, furniture_check)
            else:
                bot.send_message(message.chat.id,
                                 'Верно',
                                 parse_mode="Markdown", )
                change_answer(message.from_user, 'furniture_answer', "answer_2")
                if check_answer_final(message.from_user, 'furniture_answer'):
                    change(message.from_user, "furniture")
                    bot.send_photo(message.chat.id,
                                   'AgACAgIAAxkBAAICzWQVrj9GWMcYaaYWWXPdN4Kan-OdAAKtxzEboWeoSBaPwuII2i2-AQADAgADeQADLwQ',
                                   reply_markup=keyboard.crossworld())
                    bot.register_next_step_handler(message, furniture_end_message)
                else:
                    bot.register_next_step_handler(message, furniture_check)
        elif message.text.lower() in ['3зеркало']:
            if check_answer(message.from_user, 'furniture_answer', "answer_3"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", )
                bot.register_next_step_handler(message, furniture_check)
            else:
                bot.send_message(message.chat.id,
                                 'Верно',
                                 parse_mode="Markdown", )
                change_answer(message.from_user, 'furniture_answer', "answer_3")
                if check_answer_final(message.from_user, 'furniture_answer'):
                    change(message.from_user, "furniture")
                    bot.send_photo(message.chat.id,
                                   'AgACAgIAAxkBAAICzWQVrj9GWMcYaaYWWXPdN4Kan-OdAAKtxzEboWeoSBaPwuII2i2-AQADAgADeQADLwQ',
                                   reply_markup=keyboard.crossworld())
                    bot.register_next_step_handler(message, furniture_end_message)
                else:
                    bot.register_next_step_handler(message, furniture_check)
        elif message.text.lower() in ['4вешалка']:
            if check_answer(message.from_user, 'furniture_answer', "answer_4"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", )
                bot.register_next_step_handler(message, furniture_check)
            else:
                bot.send_message(message.chat.id,
                                 'Верно',
                                 parse_mode="Markdown", )
                change_answer(message.from_user, 'furniture_answer', "answer_4")
                if check_answer_final(message.from_user, 'furniture_answer'):
                    change(message.from_user, "furniture")
                    bot.send_photo(message.chat.id,
                                   'AgACAgIAAxkBAAICzWQVrj9GWMcYaaYWWXPdN4Kan-OdAAKtxzEboWeoSBaPwuII2i2-AQADAgADeQADLwQ',
                                   reply_markup=keyboard.crossworld())
                    bot.register_next_step_handler(message, furniture_end_message)
                else:
                    bot.register_next_step_handler(message, furniture_check)
        elif message.text.lower() in ['5диван']:
            if check_answer(message.from_user, 'furniture_answer', "answer_5"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", )
                bot.register_next_step_handler(message, furniture_check)
            else:
                bot.send_message(message.chat.id,
                                 'Верно',
                                 parse_mode="Markdown", )
                change_answer(message.from_user, 'furniture_answer', "answer_5")
                if check_answer_final(message.from_user, 'furniture_answer'):
                    change(message.from_user, "furniture")
                    bot.send_photo(message.chat.id,
                                   'AgACAgIAAxkBAAICzWQVrj9GWMcYaaYWWXPdN4Kan-OdAAKtxzEboWeoSBaPwuII2i2-AQADAgADeQADLwQ',
                                   reply_markup=keyboard.crossworld())
                    bot.register_next_step_handler(message, furniture_end_message)
                else:
                    bot.register_next_step_handler(message, furniture_check)
        elif message.text.lower() in ['клад']:
            bot.send_message(message.chat.id,
                             'Отличная работа!',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            bot.send_message(message.chat.id,
                             'Мероприятие любят не только за его наполнение, но и глазами. Потому, рекомендуем выдерживать '
                             'в любом ивенте общий стиль. Мебель и текстиль, а также интересный декор – это всегда '
                             'прекрасно.\n'
                             '\n'
                             'Возвращайся в меню 🥰',
                             parse_mode="Markdown", reply_markup=keyboard.telegram_furniture_inline())
            if check_final(message.from_user):
                end(message)
        else:
            bot.send_message(message.chat.id,
                             'Не верно',
                             parse_mode="Markdown", reply_markup=keyboard.crossworld())
            bot.register_next_step_handler(message, furniture_check)
    except Exception as error:
        print(f'furniture_check: {error}')
        bot.register_next_step_handler(message, furniture_check)


def furniture_end_message(message):
    try:
        if message.text.lower() in ['клад']:
            bot.send_message(message.chat.id,
                             'Отличная работа!',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            bot.send_message(message.chat.id,
                             'Мероприятие любят не только за его наполнение, но и глазами. Потому, рекомендуем выдерживать '
                             'в любом ивенте общий стиль. Мебель и текстиль, а также интересный декор – это всегда '
                             'прекрасно.\n'
                             '\n'
                             'Возвращайся в меню 🥰',
                             parse_mode="Markdown", reply_markup=keyboard.telegram_furniture_inline())
            if check_final(message.from_user):
                end(message)
        else:
            bot.send_message(message.chat.id,
                             'Так-так-так, расслабляться ещё рано 😊',
                             parse_mode="Markdown", reply_markup=keyboard.crossworld())
            bot.register_next_step_handler(message, furniture_end_message)
    except Exception as error:
        print(f'furniture_end_message: {error}')
        bot.register_next_step_handler(message, furniture_end_message)


@bot.message_handler(func=lambda message: message.text.lower() == 'казино' or message.text.lower() == 'казино ✅',
                     content_types=['text'])
def casino(message):
    try:
        if check(message.from_user, "furniture"):
            bot.send_message(message.chat.id,
                             'Вы проходили данное задание',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            bot.send_message(message.chat.id,
                             'Да, в нашей стране Казино и игра на деньги запрещены. Именно поэтому, наше фан-казино на то '
                             'и фан. Мы играем не на деньги, а на фишки, интерес и азарт. А ещё, все крупье – настоящие '
                             'профессионалы. Без шуток, это ребята, которые работали в настоящих казино. Они точно '
                             'знают своё дело)\n'
                             'Фан-казино, кулинарное-казино, тиры и игровые аппараты – всё, для того, чтобы создать '
                             'настоящее погружение!\n',
                             parse_mode="Markdown", reply_markup=keyboard.telegram_casino_inline())
        else:
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEIHeVkDu949s5aPydxGXaUzMKCPAfQuQAC4igAAu3QWUiJCmpWhUnbJi8E")
            bot.send_message(message.chat.id, '🧩 Надеюсь азарт от этой игры уже разыгрался, а тут ещё и тема Казино! '
                                              'Сразу скажу, что Казино у нас фановое и существует в двух вариантах: '
                                              'классика (покер, рулетка, блэкджек и другие) и кулинарное (виски-казино, '
                                              'сырное-казино, мармеладное-казино и другие).\n'
                                              '\n'
                                              '✅ _Расскажу, конечно, всё подробнее, только сначала предлагаю сыграть '
                                              'со мной в игру. Игра – русская версия Блэкджека – Двадцать Одно. Суть '
                                              'очень проста. Я раздаю карты, а тебе нужно набрать в сумме 21 или меньше '
                                              'очков, чем у меня. Проверяем интуицию. Выбери: пас или ещё?_\n',
                             parse_mode="Markdown", reply_markup=keyboard.casino_keyboard())
        bot.send_photo(message.chat.id,
                       'AgACAgIAAxkBAAICzmQVr1mnpchGiLFy07QfbRCTBcXmAAK4xzEboWeoSI2Opx-qLif-AQADAgADcwADLwQ')
        bot.send_photo(message.chat.id,
                       'AgACAgIAAxkBAAICz2QVr20kupkYXZg7vjZdjYIOGbGdAAK8xzEboWeoSHTmDCpUfARyAQADAgADeQADLwQ',
                       reply_markup=keyboard.casino_keyboard())
        bot.register_next_step_handler(message, casino_end)
    except Exception as error:
        print(f'casino: {error}')
        bot.register_next_step_handler(message, casino)


def casino_end(message):
    try:
        if message.text.lower() in ['еще', 'ещё']:
            change(message.from_user, "casino")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIC0GQVsGxi-tAcafF7paB4uDLJIdJlAALDxzEboWeoSPSsU6y5nyniAQADAgADeQADLwQ',
                           reply_markup=keyboard.keyboard(message.from_user))
            bot.send_message(message.chat.id,
                             'Так уж и быть… Отличный выбор, удача на твоей стороне! Победа, получается! 🥳\n'
                             '\n'
                             'Да, в нашей стране Казино и игра на деньги запрещены. Именно поэтому, наше фан-казино на то '
                             'и фан. Мы играем не на деньги, а на фишки, интерес и азарт. А ещё, все крупье – настоящие '
                             'профессионалы. Без шуток! Это ребята, которые работали в настоящих казино. Они точно '
                             'знают своё дело)\n'
                             'Фан-казино, кулинарное-казино, тиры и игровые аппараты – всё, для того, чтобы создать '
                             'настоящее погружение!\n'
                             '\n'
                             'Возвращайся в меню 🥰',
                             parse_mode="Markdown", reply_markup=keyboard.telegram_casino_inline())

            if check_final(message.from_user):
                end(message)
        elif message.text.lower() in ['пас']:
            change(message.from_user, "casino")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIC0WQVsYLApjHwS2V-x4dUwqLx4VU2AALHxzEboWeoSFtjgWM2FOxrAQADAgADeQADLwQ',
                           reply_markup=keyboard.keyboard(message.from_user))
            bot.send_message(message.chat.id,
                             'Ого, удача на твоей стороне! Ну ладно, я расстраиваться сегодня не буду. Победа за тобой, '
                             'получается! 🥳\n'
                             '\n'
                             'Да, в нашей стране Казино и игра на деньги запрещены. Именно поэтому, наше фан-казино на то '
                             'и фан. Мы играем не на деньги, а на фишки, интерес и азарт. А ещё, все крупье – настоящие '
                             'профессионалы. Без шуток, это ребята, которые работали в настоящих казино. Они точно '
                             'знают своё дело)\n'
                             'Фан-казино, кулинарное-казино, тиры и игровые аппараты – всё, для того, чтобы создать '
                             'настоящее погружение!\n'
                             '\n'
                             'Возвращайся в меню 🥰',
                             parse_mode="Markdown", reply_markup=keyboard.telegram_casino_inline())

            if check_final(message.from_user):
                end(message)
    except Exception as error:
        print(f'casino_end: {error}')
        bot.register_next_step_handler(message, casino_end)


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
    # rais = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    database = db.Data(user_data)
    number = database.check_final()
    # number.remove(str(user_data.id))
    if all(number):
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


def setSurname(message):
    user = db.Data(message.from_user)
    surname = message.text
    user.setSurname(surname)


def setName(message):
    user = db.Data(message.from_user)
    name = message.text
    user.setName(name)


def setPhone(message):
    user = db.Data(message.from_user)
    phone = message.text
    user.setPhone(phone)


while True:
    try:
        bot.polling(none_stop=True, timeout=10)
    except Exception as error:
        print(error)
        time.sleep(3)
