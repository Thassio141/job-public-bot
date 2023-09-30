import schedule
import db_functions

import functions

vacancy_list_name = ["AWS", "Java", "Desenvolvedor", "Estagio", "Estagiario", "Administração", "Engenheiro", "Advogado",
                     "Kotlin", "Python", "Spring", "Django", "IA", "Devops", "Gerente"]


def schedule_delete_old_data():
    schedule.every().day.at("23:50").do(db_functions.delete_old_data())


def func_web_scraping_data():
    for i in vacancy_list_name:
        functions.all_web_scraping(i)


def schedule_web_scraping():
    schedule.every().day.at("14:28").do(func_web_scraping_data)
