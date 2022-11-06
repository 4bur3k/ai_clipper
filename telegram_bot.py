import telebot
import json

with open('tokens.json') as token_file:
    token = json.load(token_file)['Tokens']['Telegram']['APIKey']
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello!')


# function to be called externally
def start_bot():
    bot.polling(none_stop=True, interval=0)
