import telebot
import functions
import db_functions
from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)


def linkedin_vacancy(message):
    if message.text is not None: 
        vacancy_name = message.text
        response = functions.find_if_not_db_scrap_linkedin(bot,message,vacancy_name)
        
        bot.send_message(message.chat.id, response)
    

@bot.message_handler(commands=['start'])
def welcome_message(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button_linkedin = telebot.types.InlineKeyboardButton("Linkedin", callback_data="button_click_linkedin")
    button_detail = telebot.types.InlineKeyboardButton("Detalhes", callback_data="button_click_detail")

    markup.add(button_linkedin,button_detail)

    bot.send_message(message.chat.id, "Olá! Clique no botão abaixo:", reply_markup=markup)

    
@bot.callback_query_handler(func=lambda msg: True)
def conditional_message_handler(msg):
    if msg.data == "button_click_linkedin":
        bot.send_message(msg.message.chat.id, "Digite o nome da vaga que você quer:")
        bot.register_next_step_handler(msg.message, linkedin_vacancy)

    if msg.data == "button_click_detail":
        bot.send_message(msg.message.chat.id, functions.detail_message())


if __name__ == '__main__':
    bot.infinity_polling()