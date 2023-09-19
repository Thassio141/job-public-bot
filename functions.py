from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import datetime
#Version 1.3

def write_log(message):
    now_datetime = datetime.datetime.now()
    hour_now = now_datetime.strftime("%Y-%m-%d %H:%M:%S")
    final_message = f"[{hour_now}] {message}"
    
    with open('log.txt', 'a') as file:
        file.write(final_message + '\n')

def welcome_message(bot,message):
    msg_text = """Olá, sou a Jobby e estou aqui para auxiliar você a encontrar sua vaga desejada!\n
Aqui vai alguns comandos que você pode usar:\n
*Não é necessario o uso de parenteses nos comandos*
Procura vagas no site da gupy:
    /gupy (nome da vaga) 
    /gupy_remoto (nome da vaga)
Procura vagas no site do linkedin:
    /linkedin (nome da vaga)
    /linkedin_remoto (nome da vaga)
Procura vagas no site do glassdoor:
    /glassdoor (nome da vaga)
    /glassdoor_remoto (nome da vaga)
Procurar vagas tanto no linkedin quanto na gupy:
    /vagas nome da vaga
    /vagas_remotas nome da vaga
    /detalhes"""
    bot.send_message(message.chat.id, msg_text)

def any_message(bot,message):
    msg_text = "Desculpe não entendi, use /start ou /help para ver os comandos válidos!"
    bot.send_message(message.chat.id, msg_text)

def detail_message(bot,message):
    msg_text = """
Atualmente estou na versão 1.1!
Informações do meu criador: https://www.linkedin.com/in/th%C3%A1ssio-vagner-6098a5215/
Github do projeto Jobby: https://github.com/Thassio141/job-public-bot 
"""
    bot.send_message(message.chat.id,msg_text)

def response_search_gupy(bot,message):
    
    mensagem_texto = message.text
    if 'remoto' in mensagem_texto:
        mensagem_separada = mensagem_texto.split('/gupy_remoto ')
        try:
            variavel = mensagem_separada[1]
            url = f'https://portal.gupy.io/job-search/term={variavel}&workplaceTypes[]=remote'
        except IndexError:
            bot.reply_to(message, f'Você precisa digitar o nome da vaga junto ao comando para poder pesquisar!')
            return 
                
    else:
        mensagem_separada = mensagem_texto.split('/gupy ')
        try:
            variavel = mensagem_separada[1]
            url = f'https://portal.gupy.io/job-search/term={variavel}'
        except IndexError:
            bot.reply_to(message, f'Você precisa digitar o nome da vaga junto ao comando para poder pesquisar!')
            return
        
    bot.reply_to(message, f'Ok! Aguarde um momento enquanto procuro as vagas! (Pode demorar até 15 segundos)')

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Não abra o navegador
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    for _ in range(3):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    cards = soup.find_all(class_='sc-a3bd7ea-0 HCzvP')
    if len(cards) > 0:
        bot.send_message(message.chat.id, f'Aqui estão algumas vagas relacionadas a {message.text}')

        for card in cards:
            title_element = card.find(class_='sc-llJcti jgKUZ sc-a3bd7ea-5 XNNQK')
            company_element = card.find(class_='sc-efBctP dpAAMR sc-a3bd7ea-6 cQyvth')
            date_element = card.find(class_='sc-efBctP dpAAMR sc-1db88588-0 inqtnx')
            link_element = card.find(class_='sc-a3bd7ea-1 kCVUJf')
            info_element = card.find_all(class_='sc-23336bc7-1 cezNaf')
            local_element = info_element[0]
            vacancy_type_element = info_element[1]
            contract_element = info_element[2]

            title = title_element.text.strip() if title_element else "N/A"
            company = company_element.text.strip() if company_element else "N/A"
            date = date_element.text.strip() if date_element else "N/A"
            link = link_element['href']
            local = local_element.text.strip() if local_element else "N/A"
            vacancy_type = vacancy_type_element.text.strip() if vacancy_type_element else "N/A"
            contract = contract_element.text.strip() if contract_element else "N/A"

            mensagem = f"Título: {title}\nEmpresa: {company}\nData: {date}\nLink: {link}\nLocal: {local}\nTipo de Vaga: {vacancy_type}\nContrato: {contract}\n"
            bot.send_message(message.chat.id, mensagem)

    else:
        bot.reply_to(message, f'Desculpe não encontrei vagas sobre {variavel}')
    driver.quit()
    bot.send_message(message.chat.id, 'Posso te ajudar em mais alguma coisa?')


def response_search_linkedin(bot,message):
    mensagem_texto = message.text
    if 'remoto' in message.text:
        mensagem_separada = mensagem_texto.split('/linkedin_remoto ')
        try:
            variavel = mensagem_separada[1]
            url = f'https://www.linkedin.com/jobs/search?keywords={variavel}&location=Brasil&locationId=&geoId=106057199&f_TPR=&f_WT=2&position=1&pageNum=0'
        except IndexError:
            bot.reply_to(message, f'Você precisa digitar o nome da vaga junto ao comando para poder pesquisar!')
            return 
    else:
        mensagem_separada = mensagem_texto.split('/linkedin ')
        try:
            variavel = mensagem_separada[1]
            url = f'https://www.linkedin.com/jobs/search?keywords={variavel}&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
        except IndexError:
            bot.reply_to(message, f'Você precisa digitar o nome da vaga junto ao comando para poder pesquisar!')
            return 
    
    bot.reply_to(message, f'Ok! Aguarde um momento enquanto procuro as vagas! (Pode demorar até 15 segundos)')

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Não abra o navegador
    options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(options=options)
    driver.get(url) 

    for _ in range(3):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    cards = soup.find_all(class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    if len(cards) > 0:
        bot.send_message(message.chat.id, f'Aqui estão algumas vagas relacionadas a {variavel}')

        for card in cards:
            title_element = card.find(class_='base-search-card__title')
            company_element = card.find(class_='base-search-card__subtitle')
            date_element = card.find(class_='job-search-card__listdate')
            link_element = card.find(class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')
            local_element = card.find(class_='job-search-card__location')

            title = title_element.text.strip() if title_element else "N/A"
            company = company_element.text.strip() if company_element else "N/A"
            date = date_element.text.strip() if date_element else "N/A"
            link = link_element['href']
            local = local_element.text.strip() if local_element else "N/A"

            if 'remoto' in message.text:
                vacancy_type_element = 'Remoto'
                mensagem = f"Título: {title}\nEmpresa: {company}\nData: {date}\nLink: {link}\nLocal: {local}\nTipo de Vaga: {vacancy_type_element}\n"

            else:
                mensagem = f"Título: {title}\nEmpresa: {company}\nData: {date}\nLink: {link}\nLocal: {local}\n"

            bot.send_message(message.chat.id, mensagem)

    else:
        bot.reply_to(message, f'Desculpe não encontrei vagas sobre {variavel}')
    driver.quit()

    bot.send_message(message.chat.id, 'Posso te ajudar em mais alguma coisa?')

def glassdoor_response(bot, message):
    mensagem_texto = message.text
    if 'remoto' in mensagem_texto:
        mensagem_separada = mensagem_texto.split('/glassdoor_remoto ')
        try:
            variavel = mensagem_separada[1]
            tamanho_var = len(variavel) + 16
            url = f'https://www.glassdoor.com.br/Vaga/trabalho-remoto-{variavel}-vagas-SRCH_IL.0,15_IS12226_KO16,{tamanho_var}.htm'
        except IndexError:
            bot.reply_to(message, f'Você precisa digitar o nome da vaga junto ao comando para poder pesquisar!')
            return 
                
    else:
        mensagem_separada = mensagem_texto.split('/glassdoor ')
        try:
            variavel = mensagem_separada[1]
            tamanho_var = len(variavel)
            url = f'https://www.glassdoor.com.br/Vaga/{variavel}-vagas-SRCH_KO0,{tamanho_var}.htm'
        except IndexError:
            bot.reply_to(message, f'Você precisa digitar o nome da vaga junto ao comando para poder pesquisar!')
            return 
    bot.reply_to(message, f'Ok! Aguarde um momento enquanto procuro as vagas! (Pode demorar até 15 segundos)')
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Não abra o navegador
    options.add_argument('window-size=1920x1080')
    agent="Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36"
    options.add_argument(f'user-agent={agent}')
    driver = webdriver.Chrome(options=options)
    driver.get(url) 

    for _ in range(3):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    cards = soup.find_all(class_='job-search-193lseq')
    if len(cards) > 0:
        for card in cards:
            title_element = card.find(class_='job-title mt-xsm')
            company_element = card.find(class_='job-search-8wag7x')
            date_element = card.find(class_='d-flex align-items-end ml-xsm listing-age')
            link_element = card.find(class_='d-flex justify-content-between p-std jobCard')
            local_element = card.find(class_='location mt-xxsm')
            #contract_element = info_element[2]

            title = title_element.text.strip() if title_element else "N/A"
            company = company_element.text.strip() if company_element else "N/A"
            date = date_element.text.strip() if date_element else "N/A"
            link = link_element['href']
            local = local_element.text.strip() if local_element else "N/A"
            #contract = contract_element.text.strip() if contract_element else "N/A"

            mensagem = f"Título: {title}\nEmpresa: {company}\nData: {date}\nLink: https://www.glassdoor.com.br/{link}\nLocal: {local}\n"
            bot.send_message(message.chat.id, mensagem)

    else:
        bot.reply_to(message, f'Desculpe não encontrei vagas sobre {variavel} no glassdoor')
    driver.quit()
    bot.send_message(message.chat.id, 'Posso te ajudar em mais alguma coisa?')

def vacancy_mix(bot,message):
    mensagem_texto = message.text
    if 'remotas' in mensagem_texto:
        mensagem_separada = mensagem_texto.split('/vagas_remotas ')
        try:
            variavel = mensagem_separada[1]
            url = f'https://portal.gupy.io/job-search/term={variavel}&workplaceTypes[]=remote'
        except IndexError:
            bot.reply_to(message, f'Você precisa digitar o nome da vaga junto ao comando para poder pesquisar!')
            return 
                
    else:
        mensagem_separada = mensagem_texto.split('/vagas ')
        try:
            variavel = mensagem_separada[1]
            url = f'https://portal.gupy.io/job-search/term={variavel}'
        except IndexError:
            bot.reply_to(message, f'Você precisa digitar o nome da vaga junto ao comando para poder pesquisar!')
            return
        
    bot.reply_to(message, f'Ok! Aguarde um momento enquanto procuro as vagas! (Pode demorar até 15 segundos)')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Não abra o navegador
    options.add_argument('window-size=1920x1080')
    agent="Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1866.237 Safari/537.36"
    options.add_argument(f'user-agent={agent}')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    for _ in range(3):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    cards = soup.find_all(class_='sc-a3bd7ea-0 HCzvP')
    if len(cards) > 0:
        bot.send_message(message.chat.id, f'Aqui estão algumas vagas relacionadas a {message.text}')
        count = 0

        for card in cards:
            count += 1
            if count == 7:
                break
            title_element = card.find(class_='sc-llJcti jgKUZ sc-a3bd7ea-5 XNNQK')
            company_element = card.find(class_='sc-efBctP dpAAMR sc-a3bd7ea-6 cQyvth')
            date_element = card.find(class_='sc-efBctP dpAAMR sc-1db88588-0 inqtnx')
            link_element = card.find(class_='sc-a3bd7ea-1 kCVUJf')
            info_element = card.find_all(class_='sc-23336bc7-1 cezNaf')
            local_element = info_element[0]
            vacancy_type_element = info_element[1]
            contract_element = info_element[2]

            title = title_element.text.strip() if title_element else "N/A"
            company = company_element.text.strip() if company_element else "N/A"
            date = date_element.text.strip() if date_element else "N/A"
            link = link_element['href']
            local = local_element.text.strip() if local_element else "N/A"
            vacancy_type = vacancy_type_element.text.strip() if vacancy_type_element else "N/A"
            contract = contract_element.text.strip() if contract_element else "N/A"

            mensagem = f"Título: {title}\nEmpresa: {company}\nData: {date}\nLink: {link}\nLocal: {local}\nTipo de Vaga: {vacancy_type}\nContrato: {contract}\n"
            bot.send_message(message.chat.id, mensagem)

    else:
        bot.reply_to(message, f'Desculpe não encontrei vagas sobre {variavel}')

    if 'remotas' in message.text:
        mensagem_separada = mensagem_texto.split('/vagas_remotas ')
        try:
            variavel = mensagem_separada[1]
            url = f'https://www.linkedin.com/jobs/search?keywords={variavel}&location=Brasil&locationId=&geoId=106057199&f_TPR=&f_WT=2&position=1&pageNum=0'
        except IndexError:
            bot.reply_to(message, f'Você precisa digitar o nome da vaga junto ao comando para poder pesquisar!')
            return 
    else:
        mensagem_separada = mensagem_texto.split('/vagas ')
        try:
            variavel = mensagem_separada[1]
            url = f'https://www.linkedin.com/jobs/search?keywords={variavel}&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
        except IndexError:
            bot.reply_to(message, f'Você precisa digitar o nome da vaga junto ao comando para poder pesquisar!')
            return 
    
    driver.get(url) 

    for _ in range(3):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    cards = soup.find_all(class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    if len(cards) > 0:
        count = 0

        for card in cards:
            count += 1
            if count == 7:
                break
            title_element = card.find(class_='base-search-card__title')
            company_element = card.find(class_='base-search-card__subtitle')
            date_element = card.find(class_='job-search-card__listdate')
            link_element = card.find(class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')
            local_element = card.find(class_='job-search-card__location')

            title = title_element.text.strip() if title_element else "N/A"
            company = company_element.text.strip() if company_element else "N/A"
            date = date_element.text.strip() if date_element else "N/A"
            link = link_element['href']
            local = local_element.text.strip() if local_element else "N/A"

            if 'remoto' in message.text:
                vacancy_type_element = 'Remoto'
                mensagem = f"Título: {title}\nEmpresa: {company}\nData: {date}\nLink: {link}\nLocal: {local}\nTipo de Vaga: {vacancy_type_element}\n"

            else:
                mensagem = f"Título: {title}\nEmpresa: {company}\nData: {date}\nLink: {link}\nLocal: {local}\n"

            bot.send_message(message.chat.id, mensagem)

    if 'remotas' in message.text:
        mensagem_separada = mensagem_texto.split('/vagas_remotas ')
        try:
            variavel = mensagem_separada[1]
            tamanho_var = len(variavel) + 16
            url = f'https://www.glassdoor.com.br/Vaga/trabalho-remoto-{variavel}-vagas-SRCH_IL.0,15_IS12226_KO16,{tamanho_var}.htm'
        except IndexError:
            bot.reply_to(message, f'Você precisa digitar o nome da vaga junto ao comando para poder pesquisar!')
            return 
                
    else:
        mensagem_separada = mensagem_texto.split('/vagas ')
        try:
            variavel = mensagem_separada[1]
            tamanho_var = len(variavel)
            url = f'https://www.glassdoor.com.br/Vaga/{variavel}-vagas-SRCH_KO0,{tamanho_var}.htm'
        except IndexError:
            bot.reply_to(message, f'Você precisa digitar o nome da vaga junto ao comando para poder pesquisar!')
            return 
        
    driver.get(url) 

    for _ in range(3):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    cards = soup.find_all(class_='job-search-193lseq')
    if len(cards) > 0:
        count = 0
        for card in cards:
            count += 1
            if count == 7:
                break
            title_element = card.find(class_='job-title mt-xsm')
            company_element = card.find(class_='job-search-8wag7x')
            date_element = card.find(class_='d-flex align-items-end ml-xsm listing-age')
            link_element = card.find(class_='d-flex justify-content-between p-std jobCard')
            local_element = card.find(class_='location mt-xxsm')
            #contract_element = info_element[2]

            title = title_element.text.strip() if title_element else "N/A"
            company = company_element.text.strip() if company_element else "N/A"
            date = date_element.text.strip() if date_element else "N/A"
            link = link_element['href']
            local = local_element.text.strip() if local_element else "N/A"
            #contract = contract_element.text.strip() if contract_element else "N/A"

            mensagem = f"Título: {title}\nEmpresa: {company}\nData: {date}\nLink: https://www.glassdoor.com.br/{link}\nLocal: {local}\n"
            bot.send_message(message.chat.id, mensagem)

    else:
        bot.reply_to(message, f'Desculpe não encontrei vagas sobre {variavel} no glassdoor')
    
    driver.quit()
    bot.send_message(message.chat.id, 'Posso te ajudar em mais alguma coisa?')
        