from functions import *
import telebot  

#Version 1.2

TOKEN = 'SEU TOKEN'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help','comandos'])
def welcome_message_explain(message):
    welcome_message(bot,message)
    write_log(f"welcome_message_explain / chat.id: {message.chat.id} / user: {message.from_user.username} / message: {message.text}")

@bot.message_handler(commands=['gupy','gupy_remoto'])
def search_job(message):
    response_search_gupy(bot,message)
    write_log(f"search_job / chat.id: {message.chat.id} / user: {message.from_user.username} / message: {message.text}")

@bot.message_handler(commands=['linkedin','linkedin_remoto'])
def search_linkedin_job(message):
    response_search_linkedin(bot,message)
    write_log(f"search_linkedin_job / chat.id: {message.chat.id} / user: {message.from_user.username} / message: {message.text}")

@bot.message_handler(commands=['glassdoor','glassdoor_remoto'])
def glassdoor(message):
    glassdoor_response(bot,message)
    write_log(f"glassdoor / chat.id: {message.chat.id} / user: {message.from_user.username} / message: {message.text}")

@bot.message_handler(commands=['vagas','vagas_remotas'])
def vacancy_mix_response(message):
    vacancy_mix(bot,message)
    write_log(f"vacancy_mix_response / chat.id: {message.chat.id} / user: {message.from_user.username} / message: {message.text}")

@bot.message_handler(commands=['detalhes'])
def detail_message_response(message):
    detail_message(bot,message)
    write_log(f"detail_message / chat.id: {message.chat.id} / user: {message.from_user.username} / message: {message.text}")

@bot.message_handler(func=lambda msg: True)
def any_message_response(message):
    any_message(bot,message)
    write_log(f"any_message / chat.id: {message.chat.id} / user: {message.from_user.username} / message: {message.text}")

bot.infinity_polling()