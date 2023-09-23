import pymongo
import log_func
from dotenv import load_dotenv
import re
import os


load_dotenv()

HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")


# fazer com que feche a conexão com o servidor server.close() em todas as funções abaixo
def add_vacancy(title, company, date, link, local, vacancy_type_element):
    server = pymongo.MongoClient(HOST)

    db = server[DB_NAME]

    collections = db[COLLECTION_NAME]
    
    json_obj = {f"titulo": f"{title}", "empresa": f"{company}", "data": f"{date}", "link": f"{link}",
                "local": f"{local}",
                "tipo_vaga": f"{vacancy_type_element}"}

    collections.insert_one(json_obj)
    
    server.close()


def verify_existing_document(vacancy_link):
    server = pymongo.MongoClient(HOST)

    db = server[DB_NAME]

    collections = db[COLLECTION_NAME]
    
    existing_json_obj = collections.find_one({"link": f"{vacancy_link}"})
    if vacancy_link is not None:
        if existing_json_obj:
            log_func.write_log("This data already exist in db " + "/ link: " + vacancy_link)
            return True

        else:
            log_func.write_log("New data add to the db " + "/ link: " + vacancy_link)
            return False
    else:
        log_func.write_log("This vacancy link is NoneType" )
    
    server.close()

        

def find_vacancy_db(bot,msg,keyword):
    bot.reply_to(msg, f'Ok! Aguarde um momento enquanto procuro as vagas! (Pode demorar até 15 segundos)')

    server = pymongo.MongoClient(HOST)

    db = server[DB_NAME]

    collections = db[COLLECTION_NAME]
    
    regex_pattern = re.compile(re.escape(keyword), re.IGNORECASE)

    filter = {"titulo": {"$regex": regex_pattern}}

    result = collections.find(filter)
            

        # Itere pelos resultados e formate cada documento
    for documento in result:
        string_formatada = f"Título: {documento['titulo']}\n" \
                        f"Empresa: {documento['empresa']}\n" \
                        f"Data de publicação: {documento['data']}\n" \
                        f"Link: {documento['link']}\n" \
                        f"Local: {documento['local']}\n" \
                        f"Tipo de vaga: {documento['tipo_vaga']}"
        bot.send_message(msg.chat.id, string_formatada)
        
    server.close()
