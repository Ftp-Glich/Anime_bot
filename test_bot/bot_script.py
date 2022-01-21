import telebot

from searcher import Searcher
from users_base import UserBase
from telebot import types

from requests import get

users_base = UserBase()
searcher = Searcher()


def clear_list(arr):
    for p in range(len(arr)):
        arr.pop()


def append_to_list(el, search_list):
    for element in search_list:
        if el == element:
            return True


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
        call.data = "Давай попробуем"
        call_back(call)
        return 0

    reindex_res(results)
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


@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    mes = "Вы пока ничего не выбрали"
    if call.data == "Давай попробуем":
        platform = users_base.get_platform(call.from_user.id)
        if platform == 0:
            ask_platform(call)
        else:
            users_base.clear_search_list(call.from_user.id)
            keyboard = []
            if platform == "mobile":
                for o in range(8):
                    for h in buttons_types[o]:
                        keyboard.append([h])
            else:
                for o in range(8):
                    keyboard.append(buttons_types[o])
            murkup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(call.message.chat.id, "Выберите жанры: ", reply_markup=murkup)
            temp = bot.send_message(call.message.chat.id, mes)
            users_base.set_message_id(call.from_user.id, temp.id)
            users_base.set_chat_id(call.from_user.id, call.message.chat.id)

    elif call.data == "mobile" or call.data == "desktop":
        users_base.add_user(call.from_user.id, call.data)
        users_base.clear_search_list(call.from_user.id)
        platform = call.data
        users_base.clear_search_list(call.from_user.id)
        keyboard = []
        if platform == "mobile":
            for o in range(8):
                for h in buttons_types[o]:
                    keyboard.append([h])
        else:
            for o in range(8):
                keyboard.append(buttons_types[o])
        murkup = types.InlineKeyboardMarkup(keyboard)
        bot.send_message(call.message.chat.id, "Выберите жанры: ", reply_markup=murkup)
        bot.send_message(call.message.chat.id, mes)
        users_base.set_message_id(call.from_user.id, call.message.message_id)
        users_base.set_chat_id(call.from_user.id, call.message.chat.id)
    elif call.data == "Очистить":
        users_base.clear_search_list(call.from_user.id)
        mes = "Вы пока ничего не выбрали"
        bot.edit_message_text(chat_id=users_base.get_chat_id(call.from_user.id),
                              message_id=users_base.get_message_id(call.from_user.id), text=mes)
    elif call.data == "more":
        users_base.set_results(call.from_user.id, reindex_res(users_base.get_results(call.from_user.id)))
        show_res(users_base.get_results(call.from_user.id), call)
    elif call.data == "again":
        users_base.clear_results(call.from_user.id)
        call.data = "Давай попробуем"
        call_back(call)

    elif call.data != "Поиск":
        if not append_to_list(call.data, users_base.get_search_list(call.from_user.id)):
            users_base.append_to_search_list(call.from_user.id, call.data)
            mes = ""
            for p in users_base.get_search_list(call.from_user.id):
                mes += p + " "
            bot.edit_message_text(chat_id=users_base.get_chat_id(call.from_user.id),
                                  message_id=users_base.get_message_id(call.from_user.id),
                                  text="Вы выбрали:" + mes)
    elif call.data == "Поиск":
        users_base.set_results(call.from_user.id, searcher.get_res(users_base.get_search_list(call.from_user.id)))
        show_res(users_base.get_results(call.from_user.id), call)


bot.polling()
