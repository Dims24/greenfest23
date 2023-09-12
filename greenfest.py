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

# @bot.message_handler(func=lambda message: message.text[:15] == 'Вернуться в нач')
@bot.message_handler(commands=['start'])
def handle_start(message):
    if (message.from_user.id == menedjer_1):
        bot.send_message(message.chat.id, 'Вам доступен экспорт', reply_markup=keyboard.export())
    else:
        info = db.Data(message.from_user)
        info.create()
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEIHd1kDu6_l3UN8qquRGL97sxH0shhzAACGCwAAnCfWEhLkKAVEv7IwC8E")
        bot.send_message(message.chat.id, 'Привет, дорогой друг! ❤️\n'
                                          '\n'
                                          'Я – специальный бот сервисной компании «Аренда Аттракционов». '
                                          'Предлагаю тебе пройти мою небольшую игру и получить скидку в 15% '
                                          'на аренду оборудования. Если готов, пиши - *да*', parse_mode="Markdown")
        bot.register_next_step_handler(message, rules)
        bot.send_message(64783167, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')
        bot.send_message(1248171558, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')
        bot.send_message(483241197, f'Бота запустил: {message.from_user.first_name}, @{message.from_user.username}')


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
    bot.delete_message(message.chat.id, message.message_id)


def rules(message):
    try:
        if message.text.lower() in ['да']:
            bot.send_message(message.chat.id,
                             "🥰 Ура! Рад, что ты здесь\n"
                             "\n"
                             "Для начала расскажу несколько правил:\n"
                             "⚡️ Справа снизу кнопка вызова меню\n"
                             "⚡️ Основная задача пройти все 4 задания\n"
                             "⚡️ Задания можно проходить в любом порядке\n"
                             "⚡️ Как только раунд решен, в меню появится галочка о прохождении\n"
                             "⚡️ Пройдя все задания, появится промокод на скидку\n"
                             "\n"
                             "Всё понятно?\n"
                             "Если да, введи своё имя\n"
                             "Если нет пиши [@natashka1026](@natashka1026)\n", parse_mode="Markdown")
            bot.register_next_step_handler(message, fio)
        else:
            bot.send_chat_action(message.chat.id, 'typing')
            bot.send_message(message.chat.id, '_Надо ввести_ *да*\n',
                             parse_mode="Markdown")
            bot.register_next_step_handler(message, rules)
    except Exception as error:
        print(f'rules: {error}')
        bot.register_next_step_handler(message, rules)

@bot.message_handler(func=lambda message: message.text.lower() == 'вернуться в меню', content_types=['text'])
def fio(message):
    try:
        if message.content_type == 'text':
            collector(message)
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEIHzFkDzxFeaWhNjihFqQaSFaZNWMzSAACWyoAAvMreEibkHdAfD2kCS8E")
            bot.send_message(message.chat.id, '⚡️ Аренда Аттракционов – сервисная компания. В 2023 году нам исполняется'
                                              ' 10 лет. Представляешь? Уже 10 лет, мы сопровождаем мероприятия!\n'
                                              '\n'
                                              'В нашем арсенале есть, кажется, всё, что нужно для качественного ивента:\n'
                                              '\n'
                                              '1) Шатры и мебель\n'
                                              '2) Стритфуд и кейтеринг\n'
                                              '3) Фан и кулинарное казино\n'
                                              '4) Игровое оборудование (VR, игровые, спортивные, ретро)\n'
                                              '5) Надувные аттракционы\n'
                                              '6) Тимбилдинги, квесты и интеллектуальные игры\n'
                                              '7) Профессиональный персонал\n'
                                              '8) Фотозоны\n'
                                              '9) Мастер-классы\n'
                                              '10) Техническое оборудование\n'
                                              '\n'
                                              'Сейчас предлагаем с помощью нескольких заданий на логику, познакомиться '
                                              'ближе с некоторыми из позиций.\n'
                                              '\n'
                                              'P.s, кстати, сейчас ты уже участвуешь в Telegram-квесте “Антиквиз” 😏\n'
                                              '\n'
                                              'Справа снизу есть квадратная кнопка с четырьмя точками, которая откроет '
                                              'меню. Нажми её!',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user))
            # bot.register_next_step_handler(message, antiquiz)
        else:
            bot.delete_message(message.chat.id, message.message_id)
            bot.send_message(message.chat.id, 'Мне нужны только твое Имя\n'
                             , parse_mode="Markdown")
            bot.register_next_step_handler(message, fio)
    except Exception as error:
        print(f'rules: {error}')
        bot.register_next_step_handler(message, fio)


@bot.message_handler(func=lambda message: message.text.lower() == 'антиквиз' or message.text.lower() == 'антиквиз ✅', content_types=['text'])
def antiquiz(message):
    try:
        if check(message.from_user, "antiquiz"):
            bot.send_message(message.chat.id,
                             'Вы проходили данное задание',
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
        else:
            bot.send_message(message.chat.id,
                             '🧩 Антиквиз – новый формат корпоративных интеллектуальных игр. Все задания Антиквиза на'
                             ' логику, потому, для прохождения потребуется только смекалка\n'
                             '\n'
                             'Тематика игры может быть абсолютно любой. Для примера, мы взяли классику - задание '
                             'по фильмам.\n'
                             '\n'
                             '✅ _Задача очень проста, внимательно посмотри на эмодзи и напиши название фильма в ответ_'
                             ,parse_mode="Markdown",)
            bot.send_photo(message.chat.id,
                           'AgACAgIAAxkBAAIBdGQUSliGbcKAQZ5N3Y3fBbdt3WqeAAIQxjEboWegSOJiFHAp2QmyAQADAgADeQADLwQ',
                           )
            bot.register_next_step_handler(message, antiquiz_two)
    except Exception as error:
        print(f'antiquiz: {error}')
        bot.register_next_step_handler(message, antiquiz)


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


@bot.message_handler(func=lambda message: message.text.lower() == 'шатры' or message.text.lower() == 'шатры ✅', content_types=['text'])
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
            bot.send_message(message.chat.id, '🧩 Ой, шатры – это вообще шикарное круглогодичное решение! У нас они все в '
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


@bot.message_handler(func=lambda message: message.text.lower() == 'мебель' or message.text.lower() == 'мебель ✅', content_types=['text'])
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


@bot.message_handler(func=lambda message: message.text.lower() == 'казино' or message.text.lower() == 'казино ✅', content_types=['text'])
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
                           'AgACAgIAAxkBAAIC0GQVsGxi-tAcafF7paB4uDLJIdJlAALDxzEboWeoSPSsU6y5nyniAQADAgADeQADLwQ',reply_markup=keyboard.keyboard(message.from_user))
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
                           'AgACAgIAAxkBAAIC0WQVsYLApjHwS2V-x4dUwqLx4VU2AALHxzEboWeoSFtjgWM2FOxrAQADAgADeQADLwQ', reply_markup=keyboard.keyboard(message.from_user))
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
    try:
        bot.send_sticker(message.chat.id,
                         "CAACAgIAAxkBAAEIHzVkDzyVU6XqbFLkRK6_y80nhMPWqgACSisAAof_eEh223V-zyr6vS8E")
        bot.send_message(message.chat.id, 'Поздравляю! 🥳\n'
                                          'Мой сегодняшний квест полностью пройден. А это значит, что я с чистой '
                                          'совестью готов вручить тебе промокод!\n'
                                          '\n'
                                          'Напиши, пожалуйста, свой номер телефона!',
                         parse_mode="Markdown")
        bot.register_next_step_handler(message, end_phone)
    except Exception as error:
        print(f'end: {error}')
        bot.register_next_step_handler(message, casino_end)

def end_phone(message):
    try:
        if message.content_type=='text':
            telephone(message)
            bot.send_sticker(message.chat.id,
                             "CAACAgIAAxkBAAEIHzFkDzxFeaWhNjihFqQaSFaZNWMzSAACWyoAAvMreEibkHdAfD2kCS8E")
            bot.send_message(message.chat.id, '❤️ Сервисная компания “Аренда Аттракционов”\n'
                                              '\n'
                                              'В наш День Рождения, хотим вручить скидку 15% тебе!\n'
                                              '\n'
                                              '🔹 *ПРОМОКОД:* ARENDA2023\n'
                                              'Подписывайся на наш telegram-канал, будь в курсе всех наших новинок!\n'
                                              '\n'
                                              '[Канал Аренды Аттракционов](https://t.me/arenda_attrakcionov)'
                                              '\n'
                                              'До новых встреч!\n'
                                              'Обнимаем!\n'
                                              '❤️',
                             parse_mode="Markdown", reply_markup=keyboard.keyboard(message.from_user), disable_web_page_preview=True)
    except Exception as error:
        print(f'end_phone: {error}')
        bot.register_next_step_handler(message, casino_end)
# def end(message):
#     bot.send_sticker(message.chat.id,
#                      "CAACAgIAAxkBAAEIHzFkDzxFeaWhNjihFqQaSFaZNWMzSAACWyoAAvMreEibkHdAfD2kCS8E")
#     bot.send_message(message.chat.id, '❤️ Сервисная компания “Аренда Аттракционов”\n'
#                                       '\n'
#                                       'В наш День Рождения, хотим вручить скидку 15% тебе!\n'
#                                       '\n'
#                                       '🔹 ПРОМОКОД: ARENDA2023\n'
#                                       'Подписывайся на наш telegram-канал, будь в курсе всех наших новинок!\n'
#                                       '\n'
#                                       '[Telegram](https://t.me/arenda_attrakcionov)'
#                                       '\n'
#                                       'До новых встреч!\n'
#                                       'Обнимаем!\n'
#                                       '❤️',
#                      parse_mode="Markdown",disable_web_page_preview=True)
#         # bot.register_next_step_handler(message, end_phone)

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

def telephone(message):
    user = db.Data(message.from_user)
    phone = message.text
    user.collection_phone(phone)

while True:
    try:
        bot.polling(none_stop=True, timeout=10)
    except Exception as error:
        print(error)
        time.sleep(3)
