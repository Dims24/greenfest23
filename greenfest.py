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

bot = telebot.TeleBot('6616549457:AAH_N8dlV20ihCGKxaOhqUNR9HgV6Kn5fYM')


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
menedjer_1 = 64783167
# menedjer_1 = 703608663

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
    if (message.from_user.id == menedjer_1):
        bot.send_message(message.chat.id, 'Вам доступен экспорт', reply_markup=keyboard.export())
    else:
        info = db.Data(message.from_user)
        info.create()
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEKSkJlAf8wjDicj1FxMdp1JVJrKoquYgACZTEAAmKeCUi6gWV5y2hgaTAE")
        bot.send_message(message.chat.id, '_Привет, дорогой друг!_\n'
                                          '\n'
                                          '_Мы подготовили для тебя квест. Впереди интересные загадки на логику, а также '
                                          'активности, которые расположены по всей территории._', parse_mode="Markdown")
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEKSn9lAhICYzX0fZrQl-hmN_Z5TwjkYgACF0YAAqUFEEjYj5lzUIFNxjAE")
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
        if (message.from_user.id == menedjer_1):
            excel_name = export_data()
            print(excel_name)
            bot.send_document(message.chat.id, InputFile(excel_name))
            os.remove(excel_name)
    except Exception as error:
        print(f'export: {error}')


@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'animation', 'voice', 'sticker'])
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
                             "CAACAgIAAxkBAAEKSkZlAgABoWZXxef8hvXfWYJNdtSikK4AAio0AAK5UQABSAOfBYq7prLiMAQ")
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
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEKSnZlAhGzFb1BWCzfNqoeKfo9R-uJsAACEjkAArpp-Eub3YPQbW7KUzAE')
                bot.send_message(message.chat.id,
                                 '_Ох уж эти люди, они так любят прятаться от моего братца Солнышка на своих пляжах. '
                                 'Но кажется эти подают своими зонтиками какие-то сигналы. Что же они говорят?\n'
                                 '\n'
                                 'Ответ напишите в формате: Ответ_\n'
                                 , parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                bot.send_animation(message.chat.id,
                                   'CgACAgIAAxkBAANkZQNFLNq22IubCJZooUDvhgLzHR0AAug_AALfaRhIfD7X0-4D5UwwBA')
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAANlZQNFU4MEVCoQ6nRkp6eJ8DpkoTIAArTMMRvfaRhIH4jTywJuzJ4BAAMCAAN5AAMwBA')
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
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEKSnZlAhGzFb1BWCzfNqoeKfo9R-uJsAACEjkAArpp-Eub3YPQbW7KUzAE')
            bot.send_message(message.chat.id,
                             '_Ох уж эти люди, они так любят прятаться от моего братца Солнышка на своих пляжах. '
                             'Но кажется эти подают своими зонтиками какие-то сигналы. Что же они говорят?\n'
                             '\n'
                             'Ответ напишите в формате: Ответ_\n'
                             , parse_mode="Markdown")
            bot.send_animation(message.chat.id,
                               'CgACAgIAAxkBAANkZQNFLNq22IubCJZooUDvhgLzHR0AAug_AALfaRhIfD7X0-4D5UwwBA')
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAANlZQNFU4MEVCoQ6nRkp6eJ8DpkoTIAArTMMRvfaRhIH4jTywJuzJ4BAAMCAAN5AAMwBA'
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
            change(message.from_user, "fire_1_2")
            bot.send_message(message.chat.id,
                             '_Молодцы. Вы на шаг ближе к открытию портала в лето_ 👍🏼 _Открывайте меню и '
                             'поехали дальше!_\n'
                             , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            bot.send_sticker(message.chat.id, get_need_sticker(message, 'fire'))
            if check_final(message.from_user):
                end(message)
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
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEKSnZlAhGzFb1BWCzfNqoeKfo9R-uJsAACEjkAArpp-Eub3YPQbW7KUzAE')
                bot.send_message(message.chat.id,
                                 '_Лето самая жаркая пора, так что дам вам свое задание связанное с тем, как вы '
                                 'люди прячетесь от жары. Запираетесь дома, смотрите фильмы под кондиционером. '
                                 'Отгадайте какой я загадал фильм поменяв все слова названия на противоположные_\n'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAANvZQNHMMoteezQaXGwJSjIDh6R0ZsAAsPMMRvfaRhIWN9K1AtLHqYBAAMCAAN5AAMwBA'
                               , reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, fire2_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Огонь 2_',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
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
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEKSnZlAhGzFb1BWCzfNqoeKfo9R-uJsAACEjkAArpp-Eub3YPQbW7KUzAE')
            bot.send_message(message.chat.id,
                             '_Лето самая жаркая пора, так что дам вам свое задание связанное с тем, как вы '
                             'люди прячетесь от жары. Запираетесь дома, смотрите фильмы под кондиционером. '
                             'Отгадайте какой я загадал фильм поменяв все слова названия на противоположные_\n'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAANvZQNHMMoteezQaXGwJSjIDh6R0ZsAAsPMMRvfaRhIWN9K1AtLHqYBAAMCAAN5AAMwBA',
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

            change(message.from_user, "fire_2_2")
            bot.send_message(message.chat.id,
                             '_Молодцы. Вы на шаг ближе к открытию портала в лето_ 👍🏼 _Открывайте меню и '
                             'поехали дальше!_\n'
                             , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            bot.send_sticker(message.chat.id, get_need_sticker(message, 'fire'))
            if check_final(message.from_user):
                end(message)
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
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEKSnZlAhGzFb1BWCzfNqoeKfo9R-uJsAACEjkAArpp-Eub3YPQbW7KUzAE')
                bot.send_message(message.chat.id,
                                 '_Настоящие коллеги должны понимать друг друга на любом языке! И даже на языке '
                                 'эмодзи. Попробуйте понять, кто же тут загадан!_\n'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAANwZQNHcAQDoFhSKCl858XEk2KK8D4AAsTMMRvfaRhIYfRxE9YEJDcBAAMCAAN5AAMwBA',
                               reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, fire3_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Огонь 3_',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
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
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEKSnZlAhGzFb1BWCzfNqoeKfo9R-uJsAACEjkAArpp-Eub3YPQbW7KUzAE')
            bot.send_message(message.chat.id,
                             '_Настоящие коллеги должны понимать друг друга на любом языке! И даже на языке '
                             'эмодзи. Попробуйте понять, кто же тут загадан!_\n'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAANwZQNHcAQDoFhSKCl858XEk2KK8D4AAsTMMRvfaRhIYfRxE9YEJDcBAAMCAAN5AAMwBA',
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

            change(message.from_user, "fire_3_2")
            bot.send_message(message.chat.id,
                             '_Молодцы. Вы на шаг ближе к открытию портала в лето_  👍🏼 _Открывайте меню и '
                             'поехали дальше!_\n'
                             , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            bot.send_sticker(message.chat.id, get_need_sticker(message, 'fire'))
            if check_final(message.from_user):
                end(message)
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
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEKSnplAhG4q6JXZwisEN6tV5PuwoVTigACWjYAAtua-UtLaF6wxMrMaTAE')
                bot.send_message(message.chat.id,
                                 '_Слышите? Ветер доносит ноты очень знакомой песни из пляжного ресторанчика\! '
                                 'Но что же это за песня?_\n'
                                 '\n'
                                 '_Ответ пишите в формате: *Исполнитель\_Название*_'
                                 , parse_mode="MarkdownV2")
                bot.send_audio(message.chat.id,
                               'CQACAgIAAxkBAANhZQNEI83wNmfl0nZ-X52gQ62yHRQAAtc_AALfaRhIY51RdvHwfhEwBA',
                               reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, air1_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Воздух 1_',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
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
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEKSnplAhG4q6JXZwisEN6tV5PuwoVTigACWjYAAtua-UtLaF6wxMrMaTAE')
            bot.send_message(message.chat.id,
                             '_Слышите? Ветер доносит ноты очень знакомой песни из пляжного ресторанчика\! '
                             'Но что же это за песня?_\n'
                             '\n'
                             '_Ответ пишите в формате: *Исполнитель\_Название*_'
                             , parse_mode="MarkdownV2")
            bot.send_audio(message.chat.id,
                           'CQACAgIAAxkBAANhZQNEI83wNmfl0nZ-X52gQ62yHRQAAtc_AALfaRhIY51RdvHwfhEwBA',
                           reply_markup=keyboard.keyboard_miss())
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

            change(message.from_user, "air_1_2")
            bot.send_audio(message.chat.id,
                           'CQACAgIAAxkBAANiZQNEaOphDH5Twf4noQteSyvOHtwAAts_AALfaRhILhxi1CN29JEwBA')
            bot.send_message(message.chat.id,
                             '_Молодцы. Вы на шаг ближе к открытию портала в лето_  👍🏼 _Открывайте меню и '
                             'поехали дальше!_\n'
                             , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            bot.send_sticker(message.chat.id, get_need_sticker(message, 'air'))
            if check_final(message.from_user):
                end(message)
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
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEKSnplAhG4q6JXZwisEN6tV5PuwoVTigACWjYAAtua-UtLaF6wxMrMaTAE')
                bot.send_message(message.chat.id,
                                 '_Вспоминать о лете мы будем еще долго, но чтобы его запомнить еще лучше и '
                                 'детальнее память нужно тренировать! Сможете вспомнить, что же спрятано на картинке?_\n'
                                 '\n'
                                 '_Ответ пишите в формате: Ответ_'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAANmZQNFwiMCcpqlMiEP4Uge4O8W7PoAArXMMRvfaRhINBbJMhJQdukBAAMCAAN5AAMwBA'
                               , reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, air2_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Воздух 2_',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
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
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEKSnplAhG4q6JXZwisEN6tV5PuwoVTigACWjYAAtua-UtLaF6wxMrMaTAE')
            bot.send_message(message.chat.id,
                             '_Вспоминать о лете мы будем еще долго, но чтобы его запомнить еще лучше и '
                             'детальнее память нужно тренировать! Сможете вспомнить, что же спрятано на картинке?_\n'
                             '\n'
                             '_Ответ пишите в формате: Ответ_'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAANmZQNFwiMCcpqlMiEP4Uge4O8W7PoAArXMMRvfaRhINBbJMhJQdukBAAMCAAN5AAMwBA',
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
            change(message.from_user, "air_2_2")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAANnZQNF6HUm2q5v8l5E0BHNr_rPXGAAArbMMRvfaRhIwE6RThQPjo8BAAMCAAN5AAMwBA')
            bot.send_message(message.chat.id,
                             '_Молодцы. Вы на шаг ближе к открытию портала в лето_  👍🏼 _Открывайте меню и '
                             'поехали дальше!_\n'
                             , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            bot.send_sticker(message.chat.id, get_need_sticker(message, 'air'))
            if check_final(message.from_user):
                end(message)
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
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEKSnhlAhG21UFRc8vSfLg0VPbs6e4kHgACXzYAAkGH-EsS0BG0h5b3iTAE')
                bot.send_message(message.chat.id,
                                 '_Представьте, что вы на пляже потеряли телефон или брошку и теперь вам нужно '
                                 'по своим следам выявить место потери. Для удобства, мы поделили пляж на сектора. '
                                 'Решив эту загадку, никакие потери не будут вам страшны!_\n'
                                 '\n'
                                 '_Ответ пишите в формате: Ответ_'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAANjZQNEsX97dkW853KxjTSK8crnL24AArHMMRvfaRhI_R89gjGad54BAAMCAAN5AAMwBA',
                               reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, earth1_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Земля 1_',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
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
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEKSnhlAhG21UFRc8vSfLg0VPbs6e4kHgACXzYAAkGH-EsS0BG0h5b3iTAE')
            bot.send_message(message.chat.id,
                             '_Представьте, что вы на пляже потеряли телефон или брошку и теперь вам нужно '
                             'по своим следам выявить место потери. Для удобства, мы поделили пляж на сектора. '
                             'Решив эту загадку, никакие потери не будут вам страшны!_\n'
                             '\n'
                             '_Ответ пишите в формате: Ответ_'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAANjZQNEsX97dkW853KxjTSK8crnL24AArHMMRvfaRhI_R89gjGad54BAAMCAAN5AAMwBA',
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
            change(message.from_user, "earth_1_2")
            bot.send_message(message.chat.id,
                             '_Молодцы. Вы на шаг ближе к открытию портала в лето_  👍🏼 _Открывайте меню и '
                             'поехали дальше!_\n'
                             , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            bot.send_sticker(message.chat.id, get_need_sticker(message, 'earth'))
            if check_final(message.from_user):
                end(message)
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
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEKSnhlAhG21UFRc8vSfLg0VPbs6e4kHgACXzYAAkGH-EsS0BG0h5b3iTAE')
                bot.send_message(message.chat.id,
                                 '_Нейросети сейчас окружают нас даже в путешествиях, помогая составить маршруты'
                                 ' или рассказывая и показывая красивые места.\n'
                                 'Здесь нейросеть попросили показать известное крылатое выражение, которое связано '
                                 'с путешествиями. Напишите какое._\n'
                                 '\n'
                                 '_Ответ присылайте в формате: Крылатое выражение _'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAANuZQNHA3LSpjrxNWO2yXHbEgAB8qgLAALCzDEb32kYSMXmjjNkyH-fAQADAgADeQADMAQ'
                               , reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, earth2_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Земля 2_',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
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
        elif message.text.lower() in ['инновация']:
            change(message.from_user, "earth_2_1")
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEKSnhlAhG21UFRc8vSfLg0VPbs6e4kHgACXzYAAkGH-EsS0BG0h5b3iTAE')
            bot.send_message(message.chat.id,
                             '_Нейросети сейчас окружают нас даже в путешествиях, помогая составить маршруты'
                             ' или рассказывая и показывая красивые места.\n'
                             'Здесь нейросеть попросили показать известное крылатое выражение, которое связано '
                             'с путешествиями. Напишите какое._\n'
                             '\n'
                             '_Ответ присылайте в формате: Крылатое выражение _'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAANuZQNHA3LSpjrxNWO2yXHbEgAB8qgLAALCzDEb32kYSMXmjjNkyH-fAQADAgADeQADMAQ',
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
        elif message.text.lower() in ["одна нога здесь, другая там","одна нога здесь другая там"]:
            change(message.from_user, "earth_2_2")
            bot.send_message(message.chat.id,
                             '_Молодцы. Вы на шаг ближе к открытию портала в лето_  👍🏼 _Открывайте меню и '
                             'поехали дальше!_\n'
                             , parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            bot.send_sticker(message.chat.id, get_need_sticker(message, 'earth'))
            if check_final(message.from_user):
                end(message)
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
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEKSnhlAhG21UFRc8vSfLg0VPbs6e4kHgACXzYAAkGH-EsS0BG0h5b3iTAE')
                bot.send_message(message.chat.id,
                                 '_Вы давно ходили в поход? Или вообще не ходили? Ничего страшного, сейчас вместе'
                                 ' к нему подготовимся. Нас ждет путешествие по горам Кавказа, 2 ночи у озера, жаркая,'
                                 ' но дождливая погода, так что возьмите с собой все, что может для этого пригодиться.'
                                 ' Ниже в стикерах можете выбрать вещи которые вам понадобиться, четырех будет '
                                 'достаточно, остальное уже собрано._'
                                 , parse_mode="Markdown")
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEKSrdlAievMcMK_16ed7RacF0pzcFZiwACvzUAAhu2-UvUOmjztTLceDAE'
                                 , reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, earth3_3)
        else:
            bot.send_message(message.chat.id,
                             '_Фото Земля 3_',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
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
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEKSnhlAhG21UFRc8vSfLg0VPbs6e4kHgACXzYAAkGH-EsS0BG0h5b3iTAE')
            bot.send_message(message.chat.id,
                             '_Вы давно ходили в поход? Или вообще не ходили? Ничего страшного, сейчас вместе'
                             ' к нему подготовимся. Нас ждет путешествие по горам Кавказа, 2 ночи у озера, жаркая,'
                             ' но дождливая погода, так что возьмите с собой все, что может для этого пригодиться.'
                             ' Ниже в стикерах можете выбрать вещи которые вам понадобиться, четырех будет '
                             'достаточно, остальное уже собрано._'
                             , parse_mode="Markdown")
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEKSrdlAievMcMK_16ed7RacF0pzcFZiwACvzUAAhu2-UvUOmjztTLceDAE'
                             , reply_markup=keyboard.keyboard_miss())
            bot.register_next_step_handler(message, earth3_3)
        else:
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, earth3_2)
    except Exception as error:
        print(f'earth3_2: {error}')
        bot.register_next_step_handler(message, earth3_2)


def earth3_3(message):
    try:
        if message.content_type == 'text':
            if message.text.lower() in ['пропустить']:
                miss(message)
        elif message.content_type == 'sticker':
            if message.sticker.file_unique_id == "AgADBTwAApA4-Es":
                if check_answer(message.chat, 'answer_sticker', "answer_1"):
                    bot.send_message(message.chat.id,
                                     '_Плавки уже были_',
                                     parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                    bot.register_next_step_handler(message, earth3_3)
                else:
                    bot.send_message(message.chat.id,
                                     '_Купальные шорты всегда пригодятся в жаркую погодку, тем более у озера '
                                     'остановки будут_',
                                     parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                    change_answer(message.chat, 'answer_sticker', "answer_1")
                    if check_answer_final(message.chat, 'answer_sticker'):
                        final_earth3_3(message)
                    else:
                        bot.register_next_step_handler(message, earth3_3)
            elif message.sticker.file_unique_id == "AgADWzwAAu0E-Us":
                if check_answer(message.chat, 'answer_sticker', "answer_2"):
                    bot.send_message(message.chat.id,
                                     '_Спальник уже был, внимательнее_',
                                     parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                    bot.register_next_step_handler(message, earth3_3)
                else:
                    bot.send_message(message.chat.id,
                                     '_Конечно да, без спальника нам не обойтись._',
                                     parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                    change_answer(message.chat, 'answer_sticker', "answer_2")
                    if check_answer_final(message.chat, 'answer_sticker'):
                        final_earth3_3(message)
                    else:
                        bot.register_next_step_handler(message, earth3_3)
            elif message.sticker.file_unique_id == "AgADcTkAAmo7-Us":
                if check_answer(message.chat, 'answer_sticker', "answer_3"):
                    bot.send_message(message.chat.id,
                                     '_Ну был же повербанк, давай другое_',
                                     parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                    bot.register_next_step_handler(message, earth3_3)
                else:
                    bot.send_message(message.chat.id,
                                     '_Мощный, думаю на пару дней его должно хватить, чтоб не остаться без связи._',
                                     parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                    change_answer(message.chat, 'answer_sticker', "answer_3")
                    if check_answer_final(message.chat, 'answer_sticker'):
                        final_earth3_3(message)
                    else:
                        bot.register_next_step_handler(message, earth3_3)
            elif message.sticker.file_unique_id == "AgADRjYAAvzQ-Es":
                if check_answer(message.chat, 'answer_sticker', "answer_4"):
                    bot.send_message(message.chat.id,
                                     '_Опять дождевик? Ты серьезно?!_',
                                     parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                    bot.register_next_step_handler(message, earth3_3)
                else:
                    bot.send_message(message.chat.id,
                                     '_Почти не занимает места и точно пригодится при непогоде, конечно берем._',
                                     parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                    change_answer(message.chat, 'answer_sticker', "answer_4")
                    if check_answer_final(message.chat, 'answer_sticker'):
                        final_earth3_3(message)
                    else:
                        bot.register_next_step_handler(message, earth3_3)
            elif message.sticker.file_unique_id == "AgADjTsAAgYhEUg":
                bot.send_message(message.chat.id,
                                 '_Какой еще сноуборд, вы смеетесь? Не февраль месяц же._',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, earth3_3)
            elif message.sticker.file_unique_id == "AgAD5TwAAsay-Es":
                bot.send_message(message.chat.id,
                                 '_Не самая необходимая вещь в походе, думаю лучше его все же оставить._',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, earth3_3)
            elif message.sticker.file_unique_id == "AgADqj0AAjzS-Es":
                bot.send_message(message.chat.id,
                                 '_Ладно бы еще пластиковая или железная была, но фарфор? Нет уж, у нас с собой специальная посуда будет._',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, earth3_3)
            elif message.sticker.file_unique_id == "AgADqDYAAqwQ-Es":
                bot.send_message(message.chat.id,
                                 '_Он конечно полезен при дожде, но все же в городе._',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, earth3_3)
            else:
                bot.send_chat_action(message.chat.id, 'typing')
                bot.send_message(message.chat.id, random.choice(incorrect))
                bot.register_next_step_handler(message, earth3_3)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, random.choice(incorrect))
            bot.register_next_step_handler(message, earth3_3)

    except Exception as error:
        print(f'earth3_3: {error}')
        bot.register_next_step_handler(message, earth3_3)


def final_earth3_3(message):
    change(message.from_user, "earth_3_2")
    bot.send_message(message.chat.id,
                     '_Молодцы. Вы на шаг ближе к открытию портала в лето_ 👍🏼 '
                     '_Открывайте меню и поехали дальше!_', parse_mode="Markdown",
                     reply_markup=keyboard.keyboard(message.from_user))
    bot.send_sticker(message.chat.id, get_need_sticker(message, 'earth'))
    if check_final(message.from_user):
        end(message)


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
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEKSnxlAhG781wuehAVBimZSbaSvjnPzwAC9T0AArW8-EtxOhdKihMcPjAE')
                bot.send_message(message.chat.id,
                                 '_Представьте, что вы попали в гости к своему другу, который только вернулся '
                                 'из отпуска. Вы очень хотите его удивить, рассказав о его отпуске вместо него. '
                                 'Для этого вам понадобится внимательность, ведь он еще не успел разобрать вещи. '
                                 'Посмотрите внимательно на комнату и попробуйте догадаться где был ваш друг._\n'
                                 '\n'
                                 '_Ответ присылайте в формате: слово. В одном сообщении ответ на один вопрос._'
                                 , parse_mode="Markdown")
                bot.send_photo(message.chat.id,
                               'AgACAgIAAxkBAANoZQNGKT3Y5Hee6RgR8PNF0est7j0AArvMMRvfaRhIpF7yIfo3B_gBAAMCAAN5AAMwBA')
                bot.send_document(message.chat.id,
                                  'BQACAgIAAxkBAANpZQNGVUmNoFrI8z47nPvSwxCN_gAD-j8AAt9pGEhZlNSqBhrWKTAE',
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
        elif message.text.lower() in ['результат']:
            change(message.from_user, "water_1_1")
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEKSnxlAhG781wuehAVBimZSbaSvjnPzwAC9T0AArW8-EtxOhdKihMcPjAE')
            bot.send_message(message.chat.id,
                             '_Представьте, что вы попали в гости к своему другу, который только вернулся '
                             'из отпуска. Вы очень хотите его удивить, рассказав о его отпуске вместо него. '
                             'Для этого вам понадобится внимательность, ведь он еще не успел разобрать вещи. '
                             'Посмотрите внимательно на комнату и попробуйте догадаться где был ваш друг._\n'
                             '\n'
                             '_Ответ присылайте в формате: слово. В одном сообщении ответ на один вопрос._'
                             , parse_mode="Markdown")
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAANoZQNGKT3Y5Hee6RgR8PNF0est7j0AArvMMRvfaRhIpF7yIfo3B_gBAAMCAAN5AAMwBA')
            bot.send_document(message.chat.id,
                              'BQACAgIAAxkBAANpZQNGVUmNoFrI8z47nPvSwxCN_gAD-j8AAt9pGEhZlNSqBhrWKTAE',
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
        elif message.text.lower() in ['сочи']:
            if check_answer(message.chat, 'answer', "answer_1"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
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
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                change_answer(message.chat, 'answer', "answer_2")
                if check_answer_final(message.chat, 'answer'):
                    final_water1_3(message)
                else:
                    bot.register_next_step_handler(message, water1_3)
        elif message.text.lower() in ['самолёт', 'на самолёте', 'самолётом', 'самолет', 'на самолете', 'самолетом']:
            if check_answer(message.chat, 'answer', "answer_3"):
                bot.send_message(message.chat.id,
                                 'Верно, но подобный ответ уже засчитан',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
                bot.register_next_step_handler(message, water1_3)
            else:
                bot.send_message(message.chat.id,
                                 'Прекрасно справляешься!',
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
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
                                 parse_mode="Markdown", reply_markup=keyboard.keyboard_miss())
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
                     '_Молодцы. Вы на шаг ближе к открытию портала в лето_ 👍🏼 '
                     '_Открывайте меню и поехали дальше!_', parse_mode="Markdown",
                     reply_markup=keyboard.keyboard(message.from_user))
    bot.send_sticker(message.chat.id, get_need_sticker(message, 'water'))
    if check_final(message.from_user):
        end(message)


# -------------Вода 2---------------------------
photo = [
    'AgACAgIAAxkBAANqZQNGoCwXHRbr07W5oO-SNzQKdAkAAr3MMRvfaRhIfD23k19KTnQBAAMCAAN5AAMwBA',
    'AgACAgIAAxkBAANrZQNGrQRQ6Ce-rKXPfDcNSJwAAUB-AAK-zDEb32kYSAUtPL1xtnSxAQADAgADeQADMAQ',
    'AgACAgIAAxkBAANsZQNGwZJahYADIQWkJsRq8uJzWOwAAr_MMRvfaRhIlyURJ6UWXKEBAAMCAAN5AAMwBA',
    'AgACAgIAAxkBAANtZQNG0I8ZjBzlp6G_GzKqjPo2olIAAsDMMRvfaRhItS-J2dm2g-cBAAMCAAN5AAMwBA'
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
                bot.send_sticker(message.chat.id,
                                 'CAACAgIAAxkBAAEKSnxlAhG781wuehAVBimZSbaSvjnPzwAC9T0AArW8-EtxOhdKihMcPjAE')
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
            bot.send_sticker(message.chat.id,
                             'CAACAgIAAxkBAAEKSnxlAhG781wuehAVBimZSbaSvjnPzwAC9T0AArW8-EtxOhdKihMcPjAE')
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
        if message.content_type == 'text':
            if message.text.lower() in ['пропустить']:
                miss(message)
        elif message.content_type == 'photo':
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
                                     '_Молодцы. Вы на шаг ближе к открытию портала в лето_ 👍🏼 _Открывай меню, '
                                     'поехали дальше_', parse_mode="Markdown",
                                     reply_markup=keyboard.keyboard(message.from_user))
                    bot.send_sticker(message.chat.id, get_need_sticker(message, 'water'))
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
                     "CAACAgIAAxkBAAEKSn9lAhICYzX0fZrQl-hmN_Z5TwjkYgACF0YAAqUFEEjYj5lzUIFNxjAE")
    bot.send_sticker(message.chat.id,
                     "CAACAgIAAxkBAAEKSkZlAgABoWZXxef8hvXfWYJNdtSikK4AAio0AAK5UQABSAOfBYq7prLiMAQ")
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


def get_need_sticker(message, task):
    user = db.Data(message.from_user)
    table = user.table()
    table = table[2:]
    if task == 'fire':
        completed_tasks = 0

        # Проверяем каждое задание и увеличиваем счетчик, если оно выполнено
        if table[4] and table[5]:
            completed_tasks += 1
        if table[14] and table[15]:
            completed_tasks += 1
        if table[18] and table[19]:
            completed_tasks += 1

        # Выполняем действие в зависимости от количества выполненных заданий
        if completed_tasks == 1:
            return 'CAACAgIAAxkBAAEKSoZlAhN-B_da5hlceynC-wEDMeaybQACdzkAAsJ--EvZihJw4QLHXTAE'
        elif completed_tasks == 2:
            return 'CAACAgIAAxkBAAEKSoplAhPoRT3l4YbhtB_tXRADrBm9RwACIz0AAmkK-UtgOHrpYpDlzDAE'
        elif completed_tasks == 3:
            return 'CAACAgIAAxkBAAEKSohlAhOC-nEhUO-_mUSErpcyVjABygACuzYAAm7k-Ev3812SKKnsUDAE'
        else:
            print("Ни одно задание не выполнено")

    elif task == 'earth':
        completed_tasks = 0

        # Проверяем каждое задание и увеличиваем счетчик, если оно выполнено
        if table[2] and table[3]:
            completed_tasks += 1
        if table[12] and table[13]:
            completed_tasks += 1
        if table[16] and table[17]:
            completed_tasks += 1

        # Выполняем действие в зависимости от количества выполненных заданий
        if completed_tasks == 1:
            return 'CAACAgIAAxkBAAEKSoxlAhQQqQZ29KYw2IS-w5_McKrWtQACcTYAAr6f-EtKXDM7ySzwNzAE'
        elif completed_tasks == 2:
            return 'CAACAgIAAxkBAAEKSo5lAhQW7g1qIOLIxxWal_jYao7eXAACKzUAAsej-UvHhW5LHh5tGjAE'
        elif completed_tasks == 3:
            return 'CAACAgIAAxkBAAEKSpBlAhQbxm1kh6jZjj4K-wABnQJKHrgAAn45AALx-fhL6jMmealKI0swBA'
        else:
            print("Ни одно задание не выполнено")

    elif task == 'water':
        completed_tasks = 0

        # Проверяем каждое задание и увеличиваем счетчик, если оно выполнено
        if table[8] and table[9]:
            completed_tasks += 1
        if table[10] and table[11]:
            completed_tasks += 1

        # Выполняем действие в зависимости от количества выполненных заданий
        if completed_tasks == 1:
            return 'CAACAgIAAxkBAAEKSpJlAhSyrJTwjLjyxBtspPXnGhmmNwACTzUAAnFj-EsyPQzF5pWYoDAE'
        elif completed_tasks == 2:
            return 'CAACAgIAAxkBAAEKSpRlAhS0-3XNB-Y6UrdcD-wLkQkupQAC7DQAAvmL-EvHjwABBMgz4lMwBA'
        else:
            print("Ни одно задание не выполнено")

    elif task == 'air':
        completed_tasks = 0

        # Проверяем каждое задание и увеличиваем счетчик, если оно выполнено
        if table[0] and table[1]:
            completed_tasks += 1
        if table[6] and table[7]:
            completed_tasks += 1

        # Выполняем действие в зависимости от количества выполненных заданий
        if completed_tasks == 1:
            return 'CAACAgIAAxkBAAEKSpZlAhT7rKOUrdqVlXkYpp8PfLixtgACrzAAAmaAAUiZ5OExs-sdeDAE'
        elif completed_tasks == 2:
            return 'CAACAgIAAxkBAAEKSphlAhT-Vn6EjhoBMVehrqjrRITv9QACGDkAAh7i-EuZnloJctgIJjAE'
        else:
            print("Ни одно задание не выполнено")


while True:
    try:
        bot.polling(none_stop=True, timeout=10)
    except Exception as error:
        print(error)
        time.sleep(3)
