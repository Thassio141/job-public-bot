from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta
import log_func
import os

load_dotenv()

HOST = os.getenv("HOST")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = MongoClient(HOST)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def verify_existing_document(link):
    query = {"link": link}
    result = collection.find_one(query)
    log_func.write_log(f'Verificação do banco de dados')

    return result is not None


def add_vacancy(title, company, date, link, local, vacancy_type_element):
    json_obj = {f"titulo": f"{title}",
                "empresa": f"{company}",
                "data": f"{date}",
                "link": f"{link}",
                "local": f"{local}",
                "tipo_vaga": f"{vacancy_type_element}"}

    result = collection.insert_one(json_obj)
    log_func.write_log(f'Vaga adicionada ao banco de dados')

    return result.inserted_id


def find_vacancy_db(keyword):
    query = {"titulo": {"$regex": f".*{keyword}.*", "$options": "i"},
             "tipo_vaga": "Presencial"}

    projection = {"titulo": 1, "empresa": 1, "link": 1, "local": 1, "tipo_vaga": 1}

    result = list(collection.find(query, projection))
    log_func.write_log(f'Função procurar vaga no banco de dados')

    return result


def find_remote_vacancy_db(keyword):
    query = {
        "titulo": {"$regex": f".*{keyword}.*", "$options": "i"},
        "tipo_vaga": "Remoto"
    }

    projection = {"titulo": 1, "empresa": 1, "link": 1, "local": 1, "tipo_vaga": 1}

    result = list(collection.find(query, projection))
    log_func.write_log(f'Função procurar vaga no banco de dados remota')

    return result


def delete_old_data():
    limit_date = datetime.now() - timedelta(days=2)

    query = {"data": {"$lt": limit_date.strftime("%Y-%m-%d %H:%M:%S")}}

    result = collection.delete_many(query)
    log_func.write_log(f'Função apagar vaga no banco de dados')

    return result.deleted_count
