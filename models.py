from flask_pymongo import PyMongo
import requests
from config import Config

mongo = PyMongo()


def guardar_recluso(data):
    # Guardar los datos del recluso en MongoDB
    recluso = mongo.db.reclusos.insert_one(data)
    return str(recluso.inserted_id)

def llamar_preprocesamiento(id_cedula):
    try:
        url = Config.PREPROCESAMIENTO_URL + str(id_cedula)
        response = requests.get(url)
        print("[✓] Preprocesamiento lanzado:", response.json())
    except Exception as e:
        print("[!] Error al llamar preprocesamiento:", str(e))

                                                                         