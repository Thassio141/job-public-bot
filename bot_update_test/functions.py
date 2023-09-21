import time
import telebot
import log_func
import requests
import schedule
import datetime
import db_functions
from bs4 import BeautifulSoup


def detail_message():
    return "Atualmente estou na versão 1.4!\n\nLinkedin: https://www.linkedin.com/in/th%C3%A1ssio-vagner-6098a5215/\n\nGithub do projeto Jobby: https://github.com/Thassio141/job-public-bot"


def links(name,receive_msg):
    if name == "linkedin":
        return f"https://www.linkedin.com/jobs/search?keywords={receive_msg.text}&location=Brasil&locationId=&geoId=106057199&f_TPR=r86400&f_WT=1&position=1&pageNum=0"
    elif name == "linkedin_remote":
        return f"https://www.linkedin.com/jobs/search?keywords={receive_msg.text}&location=Brasil&locationId=&geoId=106057199&f_TPR=r86400&f_WT=2&position=1&pageNum=0"
    elif name == "gupy":
        return f"https://portal.gupy.io/job-search/term={receive_msg.text}"
    elif name == "gupy_remote":
        return f"https://portal.gupy.io/job-search/term={receive_msg.text}&workplaceTypes[]=remote"


def schedule_function(function):
    schedule.every().day.at("8:00").do(function,log_func.write_log(f"Função {function} executada com sucesso!"))

    while True:
        schedule.run_pending()
        time.sleep(1)


def url_shortener(url):
    tinyurl_url = f'http://tinyurl.com/api-create.php?url={url}'

    response = requests.get(tinyurl_url)

    if response.status_code == 200:
        short_url = response.text
        log_func.write_log(f'URL encurtada com sucesso : {short_url}')

    else:
        log_func.write_log(f'Falha ao encurtar url : {url}')


def welcome_message(bot, message):
    markup = telebot.types.InlineKeyboardMarkup()
    button_linkedin = telebot.types.InlineKeyboardButton("Linkedin", callback_data="button_click_linkedin")
    button_detail = telebot.types.InlineKeyboardButton("Detalhes", callback_data="button_click_detail")

    markup.add(button_linkedin,button_detail)

    bot.send_message(message.chat.id, "Olá! Clique no botão abaixo:", reply_markup=markup)
    
    log_func.write_log(f'Mensagem de boas vindas enviada com sucesso / id:' + message.chat.id)


def conditional_message_handler(bot,msg):
    if msg.data == "button_click_linkedin":
        result = db_functions.find_vacancy_db(bot, msg)
        bot.send_message(msg.message.chat.id, result)
        log_func.write_log(f'Funcao vagas linkedin presencial chamada com sucesso / id:' + msg.message.chat.id)

    if msg.data == "button_click_detail":
        bot.send_message(msg.message.chat.id, detail_message())
        log_func.write_log(f'Mensagem de detalhes enviada com sucesso / id:' + msg.message.chat.id)


# Adicionar a ideia de banco de dados aqui
def web_scraping_function(bot,receive_message,url,general_card_class,title_html_class,company_html_class,link_html_class,local_html_class,vacancy_type_html_class):
    msg_text = receive_message.text

    response = requests.get(url)

    bot.reply_to(receive_message, f'Ok! Aguarde um momento enquanto procuro as vagas! (Pode demorar até 15 segundos)')

    soup = BeautifulSoup(response.text, 'html.parser')

    class_elements = soup.find_all(class_= general_card_class)

    for element in class_elements:
        title_element = element.find(class_=title_html_class)
        company_element = element.find(class_=company_html_class)
        link_element = element.find(class_=link_html_class)
        local_element = element.find(class_=local_html_class)
        vacancy_type_element = element.find(class_=vacancy_type_html_class)

        title = title_element.text.strip() if title_element else "N/A"
        company = company_element.text.strip() if company_element else "N/A"
        date = datetime.datetime.now()
        actual_hour = date.strftime("%Y-%m-%d %H:%M:%S")
        link = link_element['href'] if link_element else "N/A"
        local = local_element.text.strip() if local_element else "N/A"
        vacancy_type = vacancy_type_element.text.strip() if vacancy_type_element else "N/A"
        
        if db_functions.verify_existing_document(link):
            log_func.write_log(f'Funcao de procurar vagas feita com sucesso / id:' + receive_message.chat.id)
            return 
        
        else:
            short_link = url_shortener(link)

            response_message = f"Título: {title}\nEmpresa: {company}\nLink: {short_link}\nLocal: {local}\nTipo de Vaga: {vacancy_type}\nData: {actual_hour}\n"
            bot.send_message(receive_message.chat.id, response_message)
            db_functions.add_vacancy(title, company, actual_hour, short_link, local, vacancy_type)
            log_func.write_log(f'Funcao de procurar vagas feita com sucesso / id:' + receive_message.chat.id)

    else:
        bot.reply_to(receive_message, f'Desculpe não encontrei vagas sobre {msg_text}')
        log_func.write_log(f'Vagas nao encontradas / id:' + receive_message.chat.id)
        
    bot.send_message(receive_message.chat.id, 'Posso te ajudar em mais alguma coisa?')

    
def web_scraping_linkedin(bot,receive_message):
    msg_text = receive_message.text
    web_scraping_function(bot,receive_message,links("linkedin",msg_text),"base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card",
                        "base-search-card__title","base-search-card__subtitle","job-search-card__listdate","base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]","job-search-card__location","Presencial")


def web_scraping_linkedin_remote(bot,receive_message):
    msg_text = receive_message.text
    web_scraping_function(bot,receive_message,links("linkedin_remote",msg_text),"base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card",
                        "base-search-card__title","base-search-card__subtitle","job-search-card__listdate","base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]","job-search-card__location","Remoto")