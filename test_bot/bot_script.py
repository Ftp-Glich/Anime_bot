import telebot

from searcher import Searcher
from telebot import types

from requests import get

search_list = []

searcher = Searcher()


def clear_list(arr):
    for p in range(len(arr)):
        arr.pop()


def append_to_list(el):
    for element in search_list:
        if el == element:
            return False
    search_list.append(el)


bot = telebot.TeleBot("1995976002:AAFpCXXltTqQv0nF6fH-w-NdjK2MrpBCL6Q")

genres = [
 ["Экшен", "Боевые искусства", "Вампиры", "Война", "Гарем", "Гарем для девушек"],
 ["Гендерная интрига", "Детектив", "Дзёсэй", "Драма", "Игра", "История"],
 ["Дзёсэй", "Драма", "Игра", "История", "Кемонобито", "Киберпанк"],
 ["Комедия", "Лесби-тема", "Меха", "Мистика", "Пародия", "Повседневность"],
 ["Постапокалиптика", "Приключения", "Психология", "Романтика", "Сёдзе", "Сёнэн"],
 ["Самурайский боевик", "Этти",  "Сказка", "Спорт", "Сэйнэн", "Фантастика"],
 ["Триллер", "Ужасы", "Фэнтези", "Сверхъестественное", "Школа",  "Трагедия"],
 ["Очистить", "Поиск"]
]


def reindex_res(result):
    for o in range(21, len(result)):
        result[o - 21] = result[o]
    if len(result) >= 20:
        for p in range(len(result), len(result)-20, -1):
            result.pop()
    return result


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_photo(message.chat.id, get('https://media.kg-portal.ru/anime/k/kon/images/kon_14.jpg').content)
    murkup = types.InlineKeyboardMarkup(row_width=8)
    button = types.InlineKeyboardButton("Давай попробуем", callback_data='Давай попробуем')
    murkup.add(button)
    bot.send_message(message.chat.id, "Привет, я бот по жанровому поиску аниме, если хочешь найти что-то для себя дай\
  мне об этом знать.", reply_markup=murkup)


buttons_types = list()
for i in range(7):
    row = list()
    for j in range(6):
        row.append(types.InlineKeyboardButton(genres[i][j], callback_data=genres[i][j]))
    buttons_types.append(row)
buttons_types.append([])
buttons_types[7].append(types.InlineKeyboardButton(genres[7][0], callback_data=genres[7][0]))
buttons_types[7].append(types.InlineKeyboardButton(genres[7][1], callback_data=genres[7][1]))
mess = []
results1 = []


def show_res(results, call):
    for u in range(len(results)):
        if u < 21:
            call.data = ""
            bot.send_message(call.message.chat.id, results[u])
        else:
            break
    if len(results) == 0 or len(results) <= 21:
        bot.send_message(chat_id=call.message.chat.id,
                         text="Мы вывели все результаты")
        call.data = platform[0]
        call_back(call)
        return 0

    results = reindex_res(results)
    keyboard = list()
    row1 = list()
    row1.append(types.InlineKeyboardButton("Ещё", callback_data="more"))
    row1.append(types.InlineKeyboardButton("К выбору", callback_data="again"))
    keyboard.append(row1)
    markup2 = types.InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=call.message.chat.id, text="\
    Вывести ещё результатов или вернуться к выбору жанров?", reply_markup=markup2)


def ask_platform(call):
    buttons = [[types.InlineKeyboardButton("Телефон", callback_data="mobile")],
               [types.InlineKeyboardButton("Компьютер", callback_data="desktop")]]
    markup = types.InlineKeyboardMarkup(buttons)
    bot.send_message(chat_id=call.message.chat.id, text="\
    Какое у вас устройство?", reply_markup=markup)


is_first_usage = [True]
platform = [""]


@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    mes = "Вы пока ничего не выбрали"
    if call.data == "Давай попробуем":
        if is_first_usage[0]:
            ask_platform(call)
    elif call.data == "Очистить":
        for o in range(len(search_list) - 1):
            clear_list(search_list)
        mes = "Вы пока ничего не выбрали"
        mess[0] = bot.edit_message_text(chat_id=mess[0].chat.id, message_id=mess[0].message_id,
                                        text=mes)
    elif call.data == "mobile":
        platform[0] = call.data
        clear_list(search_list)
        keyboard = []
        for o in range(8):
            for h in buttons_types[o]:
                keyboard.append([h])
        murkup = types.InlineKeyboardMarkup(keyboard)
        bot.send_message(call.message.chat.id, "Выберите жанры: ", reply_markup=murkup)
        mess.append(bot.send_message(call.message.chat.id, mes))
    elif call.data == "desktop":
        platform[0] = call.data
        clear_list(search_list)
        keyboard = []
        for o in range(8):
            keyboard.append(buttons_types[o])
        murkup = types.InlineKeyboardMarkup(keyboard)
        bot.send_message(call.message.chat.id, "Выберите жанры: ", reply_markup=murkup)
        mess.append(bot.send_message(call.message.chat.id, mes))
    elif call.data == "more":
        reindex_res(results1[0])
        show_res(results1[0], call)
    elif call.data == "again":
        clear_list(results1[0])
        call.data = platform[0]
        call_back(call)

    elif call.data != "Поиск":
        temp = False
        for t in range(7):
            for u in range(6):
                if call.data == genres[t][u]:
                    temp = True
                    break
        if not temp:
            bot.delete_message(call.message.chat.id, call.chat.message_id)
        append_to_list(call.data)
        mes = ""
        for p in range(len(search_list)):
            mes += search_list[p] + " "
        mess[0] = bot.edit_message_text(chat_id=mess[0].chat.id, message_id=mess[0].message_id, text="Вы выбрали:\
 " + mes)
    elif call.data == "Поиск":
        clear_list(mess)
        if len(results1) == 0:
            results1.append((searcher.get_res(search_list)))
        else:
            results1[0] = (searcher.get_res(search_list))
        show_res(results1[0], call)
        is_first_usage[0] = False


bot.polling()
