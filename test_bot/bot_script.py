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




bot = telebot.TeleBot("your bot token")

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


def change_platform(call):
    buttons = [[types.InlineKeyboardButton("Да", callback_data="Change")],
               [types.InlineKeyboardButton("Нет", callback_data="Stay")]]
    markup = types.InlineKeyboardMarkup(buttons)
    bot.send_message(chat_id=call.message.chat.id, text="\
       Хотите поменять платформу?", reply_markup=markup)


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
        bot.answer_callback_query(call.id)
        platform = users_base.get_platform(call.from_user.id)
        if platform == 0:
            ask_platform(call)
        else:
            change_platform(call)

    elif call.data == "mobile" or call.data == "desktop" or call.data == "Change" or call.data == "Stay":
        if call.data == "Change" or call.data == "Stay":
            bot.answer_callback_query(call.id)
            if call.data == "Change":
                if users_base.get_platform(call.from_user.id) == "mobile":
                    users_base.set_platform(call.from_user.id, "desktop")
                else:
                    users_base.set_platform(call.from_user.id, "mobile")
            users_base.clear_search_list(call.from_user.id)
            keyboard = []
            if users_base.get_platform(call.from_user.id) == "mobile":
                for o in range(8):
                    for h in buttons_types[o]:
                        keyboard.append([h])
            else:
                for o in range(8):
                    keyboard.append(buttons_types[o])
            murkup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(call.message.chat.id, "Чтобы найти аниме для себя надо нажать на кнопку с нужным жанром\
            (выбранные жанры будут показываться в сообщении ниже), а далее нажмите кнопку поиск(рядом с сообщенимем с выбранными жанрами): ", reply_markup=murkup)
            temp = bot.send_message(call.message.chat.id, mes)
            users_base.set_message_id(call.from_user.id, temp.id)
            users_base.set_chat_id(call.from_user.id, call.message.chat.id)
        else:
            bot.answer_callback_query(call.id)
            users_base.add_user(call.from_user.id, call.data)
            users_base.clear_search_list(call.from_user.id)
            users_base.clear_search_list(call.from_user.id)
            keyboard = []
            if call.data == "mobile":
                for o in range(8):
                    for h in buttons_types[o]:
                        keyboard.append([h])
            else:
                for o in range(8):
                    keyboard.append(buttons_types[o])
            murkup = types.InlineKeyboardMarkup(keyboard)
            bot.send_message(call.message.chat.id, "Чтобы найти аниме для себя надо нажать на кнопку с нужным жанром\
            (выбранные жанры будут показываться в сообщении ниже), а далее нажмите кнопку поиск(рядом с сообщенимем с выбранными жанрами): ", reply_markup=murkup)
            temp = bot.send_message(call.message.chat.id, mes)
            users_base.set_message_id(call.from_user.id, temp.message_id)
            users_base.set_chat_id(call.from_user.id, call.message.chat.id)
    elif call.data == "Очистить":
        bot.answer_callback_query(call.id)
        users_base.clear_search_list(call.from_user.id)
        mes = "Вы пока ничего не выбрали"
        bot.edit_message_text(chat_id=users_base.get_chat_id(call.from_user.id),
                              message_id=users_base.get_message_id(call.from_user.id), text=mes)
    elif call.data == "more":
        bot.answer_callback_query(call.id)
        users_base.set_results(call.from_user.id, users_base.get_results(call.from_user.id)[21:])
        show_res(users_base.get_results(call.from_user.id), call)
    elif call.data == "again":
        bot.answer_callback_query(call.id)
        users_base.clear_results(call.from_user.id)
        change_platform(call)

    elif call.data != "Поиск":
        bot.answer_callback_query(call.id)
        if not append_to_list(call.data, users_base.get_search_list(call.from_user.id)):
            users_base.append_to_search_list(call.from_user.id, call.data)
            mes = ""
            for p in users_base.get_search_list(call.from_user.id):
                mes += p + " "
            bot.edit_message_text(chat_id=users_base.get_chat_id(call.from_user.id),
                                  message_id=users_base.get_message_id(call.from_user.id),
                                  text="Вы выбрали:" + mes)
    elif call.data == "Поиск":
        bot.answer_callback_query(call.id)
        users_base.set_results(call.from_user.id, searcher.get_res(users_base.get_search_list(call.from_user.id)))
        show_res(users_base.get_results(call.from_user.id), call)


bot.polling()
