import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Ya definidos antes:

    MONGO_URI = os.getenv("MONGO_URI")
    VALIDACION_URL = os.getenv("VALIDACION_URL")
    FAMILIARES_URL = os.getenv("FAMILIARES_URL")
    PREPROCESAMIENTO_URL = os.getenv("PREPROCESAMIENTO_URL")
