import re
import time
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
        return f"https://www.linkedin.com/jobs/search?keywords={receive_msg}&location=Brasil&locationId=&geoId=106057199&f_TPR=r86400&f_WT=1&position=1&pageNum=0"
    elif name == "linkedin_remote":
        return f"https://www.linkedin.com/jobs/search?keywords={receive_msg}&location=Brasil&locationId=&geoId=106057199&f_TPR=r86400&f_WT=2&position=1&pageNum=0"
    elif name == "gupy":
        return f"https://portal.gupy.io/job-search/term={receive_msg}"
    elif name == "gupy_remote":
        return f"https://portal.gupy.io/job-search/term={receive_msg}&workplaceTypes[]=remote"
    
def id_link_linkedin(link):
    match = re.search(r'-\d+\?', link)

    if match:
        number = match.group()
        number_without_special = number.replace('-', '').replace('?', '')
        return f"https://www.linkedin.com/jobs/view/{number_without_special}"

    else:
        print("Não foi possível encontrar um número no link.")
        
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
        return short_url


    else:
        log_func.write_log(f'Falha ao encurtar url : {url}')
        
def web_scraping_function(bot,receive_message,url,general_card_class,title_html_class,company_html_class,link_html_class,local_html_class,vacancy_type):
    msg_text = receive_message.text

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    class_elements = soup.find_all(class_= general_card_class)

    for element in class_elements:
        title_element = element.find(class_=title_html_class)
        company_element = element.find(class_=company_html_class)
        link_element = element.find(class_=link_html_class)
        local_element = element.find(class_=local_html_class)

        title = title_element.text.strip() if title_element else "N/A"
        company = company_element.text.strip() if company_element else "N/A"
        date = datetime.datetime.now()
        actual_hour = date.strftime("%Y-%m-%d %H:%M:%S")
        link = link_element['href'] if link_element else "N/A"
        local = local_element.text.strip() if local_element else "N/A"
        
        
        id_link = id_link_linkedin(link)

        if db_functions.verify_existing_document(id_link):
            log_func.write_log(f'Funcao de procurar vagas feita com sucesso / id:' + str(receive_message.chat.id))
            return 
        
        else:
            short_link = url_shortener(link)

            response_message = f"Título: {title}\nEmpresa: {company}\nLink: {short_link}\nLocal: {local}\nTipo de Vaga: {vacancy_type}\nData: {actual_hour}\n"
            bot.send_message(receive_message.chat.id, response_message)
            db_functions.add_vacancy(title, company, actual_hour, id_link, local, vacancy_type)
            log_func.write_log(f'Funcao de procurar vagas feita com sucesso / id:' + str(receive_message.chat.id))

    else:
        #erro envia essa mensagem no final de toda busca , não é pra acontecer
        bot.reply_to(receive_message, f'Desculpe não encontrei vagas sobre {msg_text}')
        log_func.write_log(f'Vagas nao encontradas / id:' + str(receive_message.chat.id))
        
    bot.send_message(receive_message.chat.id, 'Posso te ajudar em mais alguma coisa?')


def web_scraping_linkedin(bot,receive_message):
    msg_text = receive_message.text
    web_scraping_function(bot,receive_message,links("linkedin",msg_text),"base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card",
                        "base-search-card__title","base-search-card__subtitle","base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]","job-search-card__location","Presencial")


def web_scraping_linkedin_remote(bot,receive_message):
    msg_text = receive_message.text
    web_scraping_function(bot,receive_message,links("linkedin_remote",msg_text),"base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card",
                        "base-search-card__title","base-search-card__subtitle","base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]","job-search-card__location","Remoto")


def find_if_not_db_scrap_linkedin(bot,message,vacancy_name):
    db_functions.find_vacancy_db(bot,message,vacancy_name)
    if db_functions.find_vacancy_db(bot,message,vacancy_name) == None:
        web_scraping_linkedin(bot,message)