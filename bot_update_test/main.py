import telebot
import functions
from decouple import config

# Version 1.4

TOKEN = config("TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    functions.welcome_message(bot,message)


@bot.callback_query_handler(func=lambda msg: True)
def callback_handler(msg):
    functions.conditional_message_handler(bot,msg)


if __name__ == '__main__':
    bot.infinity_polling()