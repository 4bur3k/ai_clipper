import telebot
from telebot import types
import json
import os.path
import sqlite3
from sqlite3 import Error


# Connects application to database. Returns db_connection, cursor
def create_connection(db_path='../users.db'):
    try:
        db_con = sqlite3.connect(db_path)
        print('connection established')
        c = db_con.cursor()
        print('cursor created')
        return db_con, c
    except Error as e:
        print(e)
    #
    # return conn, c


STRINGS = None
DB_PATH = '../users.db'

with open('../tokens.json') as token_file:
    token = json.load(token_file)['Tokens']['Telegram']['APIKey']
bot = telebot.TeleBot(token)

with open('../strings.json') as strings_file:
    STRINGS = json.load(strings_file)


def create_database(db_path='../users.db'):
    try:
        db_con = sqlite3.connect(db_path)
        c = db_con.cursor()
        c.execute(STRINGS['sql_queries']['create_table'])
        print('table created')
        c.close()
        db_con.close()
    except Error as e:
        print(e)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, STRINGS['bot_answers']['start'])
    db_con, c = create_connection(DB_PATH)
    user_exists = c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
    if user_exists == 0:
        c.execute(f"INSERT INTO Users (Id, Status, Position) VALUES ({message.chat.id}, 'None', -1)")
        db_con.commit()
    else:
        print('User already exists')
    c.close()
    db_con.close()
    print('db closed')


@bot.message_handler(commands=['set_network'])
def set_network(message):
    db_con, c = create_connection(DB_PATH)
    user_exists = c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
    if user_exists == 1:
        c.execute(f"UPDATE Users SET Status = 'Network' WHERE Id = {message.chat.id}")
        db_con.commit()
    else:
        print('User does not exist')
    c.close()
    db_con.close()
    print('db closed')
    markup = types.ReplyKeyboardMarkup(row_width=1)
    item_button1 = types.KeyboardButton('ruDALL-E')
    item_button2 = types.KeyboardButton('Diffusion')
    markup.add(item_button1, item_button2)
    bot.send_message(message.chat.id, 'Choose the network to use.\n'
                                      'Hint: ruDALL-E is better in case of russian language', reply_markup=markup)


@bot.message_handler(commands=['set_artist'])
def set_artist(message):
    db_con, c = create_connection(DB_PATH)
    user_exists = c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
    if user_exists == 1:
        c.execute(f"UPDATE Users SET Status = 'Artist' WHERE Id = {message.chat.id}")
        db_con.commit()
    else:
        print('User does not exist')
    c.close()
    db_con.close()
    print('db closed')

    bot.send_message(message.chat.id, 'Write the artist\'s name:')


@bot.message_handler(commands=['set_song'])
def set_song(message):
    db_con, c = create_connection(DB_PATH)
    user_exists = c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
    if user_exists == 1:
        c.execute(f"UPDATE Users SET Status = 'Song' WHERE Id = {message.chat.id}")
        db_con.commit()
    else:
        print('User does not exist')
    c.close()
    db_con.close()
    print('db closed')
    bot.send_message(message.chat.id, 'Write the song title:')


@bot.message_handler(commands=['set_style'])
def set_style(message):
    db_con, c = create_connection(DB_PATH)
    user_exists = c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
    if user_exists == 1:
        c.execute(f"UPDATE Users SET Status = 'Style' WHERE Id = {message.chat.id}")
        db_con.commit()
    else:
        print('User does not exist')
    c.close()
    db_con.close()
    print('db closed')
    bot.send_message(message.chat.id, 'Write the style, you want to use:')


@bot.message_handler(commands=['clip'])
def msg(message):
    bot.send_message(message.chat.id, STRINGS['bot_answers']['clip_command'])


@bot.message_handler(content_types=['text'])
def start(message):

    bot.send_message(message.chat.id, 'start')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    db_con, c = create_connection(DB_PATH)

    user_exists = c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
    if user_exists == 0:
        bot.send_message(message.chat.id, STRINGS['bot_answers']['no_user_reply'])
    else:
        print('User already exists')
        status = c.execute(f"SELECT Status FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
        if status == 'Artist':
            c.execute(f"UPDATE Users SET Artist = {repr(message.text)}, Status = 'None' WHERE Id = {message.chat.id}")
        elif status == 'Song':
            c.execute(f"UPDATE Users SET Song = {repr(message.text)}, Status = 'None' WHERE Id = {message.chat.id}")
        elif status == 'Network':
            if message.text == 'ruDALL-E' or message.text == 'Diffusion':
                c.execute(
                    f"UPDATE Users SET Network = {repr(message.text)}, Status = 'None' WHERE Id = {message.chat.id}")
            else:
                c.execute(f"UPDATE Users SET Status = 'None' WHERE Id = {message.chat.id}")
                print('AAAAA, naebalovo!!!')

        elif status == 'Style':
            c.execute(f"UPDATE Users SET Style = {repr(message.text)}, Status = 'None' WHERE Id = {message.chat.id}")
        else:
            print('status is not recognized')
        db_con.commit()
        print(f'Set {status} == {message.text}')
        bot.send_message(message.chat.id, f'Set {status} = {message.text}')
    c.close()
    db_con.close()


if not os.path.isfile(DB_PATH):
    create_database(DB_PATH)

bot.polling(none_stop=True, interval=0)
