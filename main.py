from functions import *
import telebot  

#Version 1.1 alpha test

TOKEN = 'SEU TOKEN'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help','comandos'])
def welcome_message_explain(message):
    welcome_message(bot,message)

@bot.message_handler(commands=['gupy','gupy_remoto'])
def search_job(message):
    response_search_gupy(bot,message)

@bot.message_handler(commands=['linkedin','linkedin_remoto'])
def search_linkedin_job(message):
    response_search_linkedin(bot,message)

@bot.message_handler(commands=['detalhes'])
def detail_message_response(message):
    detail_message(bot,message)

@bot.message_handler(commands=['vagas','vagas_remotas'])
def vacancy_mix_response(message):
    vacancy_mix(bot,message)

@bot.message_handler(func=lambda msg: True)
def any_message_response(message):
    any_message(bot,message)

bot.infinity_polling()