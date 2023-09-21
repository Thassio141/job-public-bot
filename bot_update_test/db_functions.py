import pymongo
from decouple import config
from log_func import write_log


HOST = config("HOST")
DB_NAME = config("DB_NAME")
COLLECTION_NAME = config("COLLECTION_NAME")


def config_db():


    return 

# fazer com que feche a conexão com o servidor server.close() em todas as funções abaixo
def add_vacancy(title, company, date, link, local, vacancy_type_element):
    server = pymongo.MongoClient(HOST)

    db = server[DB_NAME]

    collections = db[COLLECTION_NAME]
    
    json_obj = {f"titulo": f"{title}", "empresa": f"{company}", "data": f"{date}", "link": f"{link}",
                "local": f"{local}",
                "tipo_vaga": f"{vacancy_type_element}"}

    collections.insert_one(json_obj)


def verify_existing_document(vacancy_link):
    server = pymongo.MongoClient(HOST)

    db = server[DB_NAME]

    collections = db[COLLECTION_NAME]
    
    existing_json_obj = collections.find_one({"link": f"{vacancy_link}"})

    if existing_json_obj:
        write_log("This data already exist in db " + "/ link: " + vacancy_link)
        return

    else:
        write_log("New data add to the db " + "/ link: " + vacancy_link)


def find_vacancy_db(bot,message):
    server = pymongo.MongoClient(HOST)

    db = server[DB_NAME]

    collections = db[COLLECTION_NAME]
    
    query = {"titulo": {"$regex": "java", "$options": "i"}}
    
    result = collections.find(query)
    
    formatted_result = ""
    for vacancy in result:
        formatted_result += f'{vacancy}\n'

    return formatted_result