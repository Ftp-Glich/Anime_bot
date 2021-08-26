import telebot

from telebot import types

import random

from requests import get


bot = telebot.TeleBot("1995976002:AAFpCXXltTqQv0nF6fH-w-NdjK2MrpBCL6Q")
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_photo(message.chat.id, get('https://media.kg-portal.ru/anime/k/kon/images/kon_14.jpg').content)
    bot.reply_to(message, "Привет, напиши Популярное, если хочшь увидеть топ 10 популярных на данный момент аниме, напиши от 1 до 3 из следующих жанров если хочешь найти аниме именно для себя(Комедия, Драма, Сёнен)")
    markup = types.ReplyKeyboardMarkup()
    itembtna = types.KeyboardButton('Комедия')
    itembtnv = types.KeyboardButton('Драма')
    itembtnc = types.KeyboardButton('Сёнен')
    itembtnd = types.KeyboardButton('Популярное')
    markup.row(itembtna, itembtnv)
    markup.row(itembtnc, itembtnd)
    bot.send_message(message.chat.id, "Выберите жанр:", reply_markup=markup)



bot.polling()