import telebot
from telebot import types
import json
import os.path
import sqlite3
from sqlite3 import Error


# Connects application to database
def create_connection(db_path='users.db'):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        print('con established')
        return conn
    except Error as e:
        print(e)

    return conn


STRINGS = None
DB_CONNECTION = None

with open('tokens.json') as token_file:
    token = json.load(token_file)['Tokens']['Telegram']['APIKey']
bot = telebot.TeleBot(token)

with open('strings.json') as strings_file:
    STRINGS = json.load(strings_file)


def create_table(db_con):
    try:
        c = db_con.cursor()
        c.execute(STRINGS['sql_queries']['create_table'])
        print('table created')
    except Error as e:
        print(e)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, STRINGS['bot_answers']['start'])


@bot.message_handler(commands=['set_network'])
def handle_text(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    item_button1 = types.KeyboardButton('ruDALL-E')
    item_button2 = types.KeyboardButton('Diffusion')
    item_button3 = types.KeyboardButton('MidJourney')
    markup.add(item_button1, item_button2, item_button3)
    bot.send_message(message.chat.id, 'Choose the network to use.\n'
                                      'Hint: ruDALL-E is better in case of russian language', reply_markup=markup)
    try:
        if message == 'ruDALL-E':
            answer = STRINGS['bot_answers']['rudalle_choice']
            pass
        elif message == 'Diffusion':
            answer = STRINGS['bot_answers']['diffusion_choice']
            pass
        elif message == 'MidJourney':
            answer = STRINGS['bot_answers']['midjourney_choice']
            pass

        neural_network_chosen = message
        bot.send_message(message.chat.id, answer + '\nNow write the artist\'s name')
    except Exception as e:
        return e


@bot.message_handler(commands=['set_artist'])
def msg(message):
    bot.send_message(message.chat.id, 'write the artist\'s name:')


@bot.message_handler(commands=['set_song'])
def msg(message):
    bot.send_message(message.chat.id, 'write the song title:')


@bot.message_handler(commands=['clip'])
def msg(message):
    bot.send_message(message.chat.id, STRINGS['bot_answers']['clip_command'])


@bot.message_handler(content_types=['text'])
def start(message):

    bot.send_message(message.chat.id, 'start')


if not os.path.isfile('users.db'):
    DB_CONNECTION = create_connection()
    create_table(DB_CONNECTION)
else:
    DB_CONNECTION = create_connection()

bot.polling(none_stop=True, interval=0)
