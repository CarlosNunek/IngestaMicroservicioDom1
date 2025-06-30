from flask_pymongo import PyMongo

mongo = PyMongo()


def guardar_recluso(data):
    # Guardar los datos del recluso en MongoDB
    recluso = mongo.db.reclusos.insert_one(data)
    return str(recluso.inserted_id)
