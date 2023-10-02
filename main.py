import os
import time
import telebot
import schedule
import functions
import db_functions
from threading import Thread
from dotenv import load_dotenv

import schedule_func
from shortener import url_shortener

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


def vacancy(message):
    if message.text is not None:
        vacancy_name = message.text
        bot.send_message(message.chat.id, "Procurando vagas aguarde um momento!")
        results = db_functions.find_vacancy_db(vacancy_name)
        if not results:
            print("não encontrei no banco")
            functions.all_web_scraping(vacancy_name)
            results = db_functions.find_vacancy_db(vacancy_name)
            for result in results:
                short_link = url_shortener(result['link'])
                response_message = (f"Título: {result['titulo']}\nEmpresa: {result['empresa']}\nLink: {short_link}"
                                    f"\nLocal: {result['local']}\nTipo: {result['tipo_vaga']}")
                bot.send_message(message.chat.id, response_message)
        else:
            print("encontrou no banco")
            for result in results:
                short_link = url_shortener(result['link'])
                response_message = (f"Título: {result['titulo']}\nEmpresa: {result['empresa']}\nLink: {short_link}"
                                    f"\nLocal: {result['local']}\nTipo: {result['tipo_vaga']}")
                bot.send_message(message.chat.id, response_message)


def vacancy_remote(message):
    if message.text is not None:
        vacancy_name = message.text
        bot.send_message(message.chat.id, "Procurando vagas aguarde um momento!")
        results = db_functions.find_remote_vacancy_db(vacancy_name)
        if not results:
            print("não encontrei no banco")
            functions.all_web_scraping(vacancy_name)
            results = db_functions.find_remote_vacancy_db(vacancy_name)
            for result in results:
                short_link = url_shortener(result['link'])
                response_message = (f"Título: {result['titulo']}\nEmpresa: {result['empresa']}\nLink: {short_link}"
                                    f"\nLocal: {result['local']}\nTipo: {result['tipo_vaga']}")
                bot.send_message(message.chat.id, response_message)
        else:
            print("encontrou no banco")
            for result in results:
                short_link = url_shortener(result['link'])
                response_message = (f"Título: {result['titulo']}\nEmpresa: {result['empresa']}\nLink: {short_link}"
                                    f"\nLocal: {result['local']}\nTipo: {result['tipo_vaga']}")
                bot.send_message(message.chat.id, response_message)


@bot.message_handler(commands=['start'])
def welcome_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button_vacancy = telebot.types.InlineKeyboardButton("Vagas Presenciais", callback_data="button_click_vacancy")
    button_vacancy_remote = telebot.types.InlineKeyboardButton("Vagas Remotas",
                                                               callback_data="button_click_vacancy_remote")
    button_detail = telebot.types.InlineKeyboardButton("Detalhes", callback_data="button_click_detail")

    markup.add(button_vacancy, button_vacancy_remote, button_detail)

    bot.send_message(message.chat.id,
                     "Olá! Eu sou a Jobby e estou aqui para auxiliar você a encontrar a sua vaga desejada"
                     "\nClique em um dos botões para começar:", reply_markup=markup)


@bot.callback_query_handler(func=lambda msg: True)
def conditional_message_handler(msg):
    if msg.data == "button_click_vacancy":
        bot.send_message(msg.message.chat.id,
                         "Digite o nome da vaga que você quer procurar:\n(Seja objetivo e não utilize nome de cidades)")
        bot.register_next_step_handler(msg.message, vacancy)

    if msg.data == "button_click_vacancy_remote":
        bot.send_message(msg.message.chat.id, "Digite o nome da vaga que você quer procurar:")
        bot.register_next_step_handler(msg.message, vacancy_remote)

    if msg.data == "button_click_detail":
        bot.send_message(msg.message.chat.id, functions.detail_message())


def schedule_checker():
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    schedule.every().day.at("11:00").do(schedule_func.func_web_scraping_data)
    schedule.every().day.at("17:00").do(schedule_func.func_web_scraping_data)
    schedule.every().day.at("23:55").do(schedule_func.schedule_delete_old_data)
    Thread(target=schedule_checker).start()
    bot.infinity_polling()
