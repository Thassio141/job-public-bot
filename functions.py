import requests
import datetime
import db_functions
from bs4 import BeautifulSoup
from shortener import id_link_linkedin


# Bug de todas as vagas e coloca como presencial ainda continua
def all_web_scraping(message):
    web_scraping_linkedin_remote(message)
    web_scraping_linkedin(message)
    web_scraping_gupy_remote(message)
    web_scraping_gupy(message)


def web_scraping_linkedin(message):
    web_scraping(
        f"https://www.linkedin.com/jobs/search?keywords={message}&location=Brasil&locationId=&geoId=106057199&f_TPR=r86400&f_WT=1&position=1&pageNum=0",
        "base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card",
        "base-search-card__title",
        "base-search-card__subtitle",
        "base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]",
        "job-search-card__location",
        "Presencial")


# Descobrir porque está salvando apenas Presencial ao invés de Remoto
def web_scraping_linkedin_remote(message):
    web_scraping(
        f"https://www.linkedin.com/jobs/search?keywords={message}&location=Brasil&locationId=&geoId=106057199&f_TPR=r86400&f_WT=2&position=1&pageNum=0",
        "base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card",
        "base-search-card__title",
        "base-search-card__subtitle",
        "base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]",
        "job-search-card__location",
        "Remoto")


def web_scraping_gupy(message):
    web_scraping(f"https://portal.gupy.io/job-search/term={message}&workplaceTypes[]=on-site",
                 "sc-a3bd7ea-0 HCzvP",
                 "sc-llJcti jgKUZ sc-a3bd7ea-5 XNNQK",
                 "sc-efBctP dpAAMR sc-a3bd7ea-6 cQyvth",
                 "sc-a3bd7ea-1 kCVUJf",
                 "sc-23336bc7-1 cezNaf",
                 "Presencial")


def web_scraping_gupy_remote(message):
    web_scraping(f"https://portal.gupy.io/job-search/term={message}&workplaceTypes[]=remote",
                 "sc-a3bd7ea-0 HCzvP",
                 "sc-llJcti jgKUZ sc-a3bd7ea-5 XNNQK",
                 "sc-efBctP dpAAMR sc-a3bd7ea-6 cQyvth",
                 "sc-a3bd7ea-1 kCVUJf",
                 "sc-23336bc7-1 cezNaf",
                 "Remoto")


def web_scraping(url, general_card_class, title_html_class, company_html_class, link_html_class,
                 local_html_class, vacancy_type):
    date = datetime.datetime.now()

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    class_elements = soup.find_all(class_=general_card_class)

    for element in class_elements:
        title_element = element.find(class_=title_html_class)
        company_element = element.find(class_=company_html_class)
        link_element = element.find(class_=link_html_class)
        local_element = element.find(class_=local_html_class)

        title = title_element.text.strip() if title_element else "N/A"
        company = company_element.text.strip() if company_element else "N/A"
        actual_hour = date.strftime("%Y-%m-%d %H:%M:%S")
        link = link_element['href'] if link_element else "N/A"
        local = local_element.text.strip() if local_element else "N/A"

        if "linkedin" in link:
            id_link = id_link_linkedin(link)
            print(id_link)

            if not id_link:
                pass

            else:
                if db_functions.verify_existing_document(id_link):
                    print("já existe um link desse no banco")
                    pass
                else:
                    db_functions.add_vacancy(title, company, actual_hour, id_link, local, vacancy_type)
                    print("Não existe um link desse no banco")

        elif "gupy" in link:
            print(link)
            if not link:
                pass
            else:
                if db_functions.verify_existing_document(link):
                    print("já existe um link desse no banco")
                    pass
                else:
                    db_functions.add_vacancy(title, company, actual_hour, link, local, vacancy_type)
                    print("Não existe um link desse no banco")


def detail_message():
    return ("Atualmente estou na versão 1.4!\n\nLinkedin: "
            "https://www.linkedin.com/in/th%C3%A1ssio-vagner-6098a5215/\n\nGithub do projeto Jobby: "
            "https://github.com/Thassio141/job-public-bot")
