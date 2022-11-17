import telebot
from telebot import types
import json

with open('tokens.json') as token_file:
    token = json.load(token_file)['Tokens']['Telegram']['APIKey']
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! This Bot will make a clip (actually a slideshow) for your song, '
                                      'using the open image generating neural networks.\n\n'
                                      'In order to start, we want you to answer some questions.'
                                      'You can answer them using the command "/set_network", "/set_artist", "/set_song".'
                                      '\n\nYou can start the process of creating a clip wit "/clip" command.')


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
            answer = 'You\'ve chosen ruDALL-E to handle your video clip'
            pass
        elif message == 'Diffusion':
            answer = 'You\'ve chosen Diffusion to handle your video clip'
            pass
        elif message == 'MidJourney':
            answer = 'You\'ve chosen MidJourney to handle your video clip'
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
    bot.send_message(message.chat.id, 'The clipping process has started.\n'
                                      'Your place in the queue: NaN')


@bot.message_handler(content_types=['text'])
def start(message):

    bot.send_message(message.chat.id, '')


bot.polling(none_stop=True, interval=0)
