import telebot
from telebot import types
import json
import os.path
import sqlite3
from sqlite3 import Error
import logging
from ClipMaker import ClipMaker


# Connects application to database. Returns db_connection, cursor
def create_connection(db_path='../users.db'):
    try:
        db_con = sqlite3.connect(db_path)
        c = db_con.cursor()
        logging.info('Connection to DB established')
        return db_con, c
    except Error as e:
        logging.exception(e)


DB_PATH = '../users.db'
logging.basicConfig(filename='ai_clipper.log',
                    format='%(asctime)s %(levelname)s:%(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    encoding='utf-8',
                    level=logging.INFO)

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
        logging.info('DB Table created')
        c.close()
        db_con.close()
    except Error as e:
        logging.error(e)


@bot.message_handler(commands=['start'])
def start(message):
    db_con, c = create_connection(DB_PATH)
    user_exists = bool(c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0])
    reply = STRINGS['bot_answers']['start']
    if not user_exists:
        c.execute(f"INSERT INTO Users (Id, Position) VALUES ({message.chat.id}, -1)")
        db_con.commit()
    status = c.execute(f"SELECT Status FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
    if status == 'Clip':
        user_pos = c.execute(f"SELECT Position FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
        reply = STRINGS['bot_answers']['clip_command'].format(value=user_pos)
    c.close()
    db_con.close()
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['set_network'])
def set_network(message):
    db_con, c = create_connection(DB_PATH)
    user_exists = bool(c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0])
    markup = None
    if user_exists:
        status = c.execute(f"SELECT Status FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
        if status == 'Clip':
            user_pos = c.execute(f"SELECT Position FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
            reply = STRINGS['bot_answers']['clip_command'].format(value=user_pos)
        else:
            c.execute(f"UPDATE Users SET Status = 'Network' WHERE Id = {message.chat.id}")
            db_con.commit()
            reply = 'Choose the network to use.\nHint: ruDALL-E is better in case of russian language'
            markup = types.ReplyKeyboardMarkup(row_width=1)
            item_button1 = types.KeyboardButton('ruDALL-E')
            item_button2 = types.KeyboardButton('StableDiffusion')
            markup.add(item_button1, item_button2)
    else:
        logging.info(f'User {message.chat.username}:{message.chat.id} does not exist in DB')
        reply = STRINGS['bot_answers']['no_user_reply']
    c.close()
    db_con.close()
    bot.send_message(message.chat.id, reply, reply_markup=markup)


@bot.message_handler(commands=['set_artist'])
def set_artist(message):
    db_con, c = create_connection(DB_PATH)
    user_exists = bool(c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0])
    if user_exists:
        status = c.execute(f"SELECT Status FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
        if status == 'Clip':
            user_pos = c.execute(f"SELECT Position FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
            reply = STRINGS['bot_answers']['clip_command'].format(value=user_pos)
        else:
            c.execute(f"UPDATE Users SET Status = 'Artist' WHERE Id = {message.chat.id}")
            db_con.commit()
            reply = 'Write the artist\'s name:'
    else:
        logging.info(f'User {message.chat.username}:{message.chat.id} does not exist in DB')
        reply = STRINGS['bot_answers']['no_user_reply']
    c.close()
    db_con.close()
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['set_song'])
def set_song(message):
    db_con, c = create_connection(DB_PATH)
    user_exists = bool(c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0])
    if user_exists:
        status = c.execute(f"SELECT Status FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
        if status == 'Clip':
            user_pos = c.execute(f"SELECT Position FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
            reply = STRINGS['bot_answers']['clip_command'].format(value=user_pos)
        else:
            c.execute(f"UPDATE Users SET Status = 'Song' WHERE Id = {message.chat.id}")
            db_con.commit()
            reply = 'Write the song title:'
    else:
        logging.info(f'User {message.chat.username}:{message.chat.id} does not exist in DB')
        reply = STRINGS['bot_answers']['no_user_reply']
    c.close()
    db_con.close()
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['set_style'])
def set_style(message):
    db_con, c = create_connection(DB_PATH)
    user_exists = bool(c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0])
    if user_exists:
        status = c.execute(f"SELECT Status FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
        if status == 'Clip':
            user_pos = c.execute(f"SELECT Position FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
            reply = STRINGS['bot_answers']['clip_command'].format(value=user_pos)
        else:
            c.execute(f"UPDATE Users SET Status = 'Style' WHERE Id = {message.chat.id}")
            db_con.commit()
            reply = 'Write the style, you want to use:'
    else:
        logging.info(f'User {message.chat.username}:{message.chat.id} does not exist in DB')
        reply = STRINGS['bot_answers']['no_user_reply']
    c.close()
    db_con.close()
    bot.send_message(message.chat.id, reply)


@bot.message_handler(commands=['clip'])
def clip(message):
    db_con, c = create_connection(DB_PATH)
    user_exists = bool(c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0])
    if not user_exists:  # user doesn't exist in DB
        reply = STRINGS['bot_answers']['no_user_reply']
    else:  # user exists in DB
        status = c.execute(f"SELECT Status FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
        if status == 'Clip':
            user_pos = c.execute(f"SELECT Position FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
            reply = STRINGS['bot_answers']['clip_command'].format(value=user_pos)
        else:
            user_data = c.execute(f"SELECT * FROM Users WHERE Id = {message.chat.id}").fetchone()
            if user_data[1] is not None and user_data[2] is not None:  # there IS enough data to start clipping
                max_pos = c.execute(f"SELECT MAX(Position) FROM Users WHERE NOT Id = {message.chat.id}").fetchone()[0]
                if max_pos == -1:
                    max_pos += 1
                if user_data[3] is not None:  # there is also a network chosen
                    c.execute(f"UPDATE Users SET Position = {max_pos + 1},"
                              f"Status = 'Clip' WHERE Id = {message.chat.id}")
                    reply = STRINGS['bot_answers']['clip_command'].format(value=max_pos + 1)
                else:
                    c.execute(
                        f"UPDATE Users SET Position = {max_pos + 1}, Status = 'Clip',"
                        f"Network = 'ruDALL-E' WHERE Id = {message.chat.id}")
                    reply = STRINGS['bot_answers']['clip_command'].format(value=max_pos + 1) + '\nSince you haven' \
                                                                                               '\'t chosen the ' \
                                                                                               'network, DALL-E is' \
                                                                                               ' used by default'
                db_con.commit()
                logging.info(f'User {message.chat.username}:{message.chat.id} is clipping. {user_data}')

                clip_maker = ClipMaker(artist=user_data[1], song=user_data[2])
                lyrics = clip_maker.get_song_text()
                reply += f'\n\n{lyrics[0]}'

            else:
                reply = 'Whoops! Seems like you haven\'t set the artist or the song you want to clip.\nUse at least' \
                        ' /set_artist and /set_song to make clipping possible.'
    bot.send_message(message.chat.id, reply)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    db_con, c = create_connection(DB_PATH)
    user_exists = bool(c.execute(f"SELECT COUNT(1) FROM Users WHERE Id = {message.chat.id}").fetchone()[0])

    if not user_exists:
        reply = STRINGS['bot_answers']['no_user_reply']
    else:
        status = c.execute(f"SELECT Status FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
        if status == 'Artist':
            c.execute(f"UPDATE Users SET Artist = {repr(message.text)}, Status = NULL WHERE Id = {message.chat.id}")
            reply = f'The artist, you\'ve chosen is {message.text}'
        elif status == 'Song':
            c.execute(f"UPDATE Users SET Song = {repr(message.text)}, Status = NULL WHERE Id = {message.chat.id}")
            reply = f'The song to be clipped: {message.text}'
        elif status == 'Network':
            if message.text == 'ruDALL-E' or message.text == 'StableDiffusion':
                c.execute(
                    f"UPDATE Users SET Network = {repr(message.text)}, Status = NULL WHERE Id = {message.chat.id}")
                reply = f'Set the network: {message.text}'
            else:
                c.execute(f"UPDATE Users SET Status = NULL WHERE Id = {message.chat.id}")
                reply = f'Such network as "{message.text}" does not exist'

        elif status == 'Style':
            c.execute(f"UPDATE Users SET Style = {repr(message.text)}, Status = NULL WHERE Id = {message.chat.id}")
            reply = f'Set style: {message.text}'
        elif status == 'Clip':
            user_pos = c.execute(f"SELECT Position FROM Users WHERE Id = {message.chat.id}").fetchone()[0]
            reply = STRINGS['bot_answers']['clip_command'].format(value=user_pos)
        else:
            logging.info('Status is not recognized')
            reply = 'Use the listed commands to add the information needed'
        db_con.commit()
    bot.send_message(message.chat.id, reply, reply_markup=types.ReplyKeyboardRemove())
    c.close()
    db_con.close()


if not os.path.isfile(DB_PATH):
    create_database(DB_PATH)

logging.info('Bot started')
bot.polling(none_stop=True, interval=0)
