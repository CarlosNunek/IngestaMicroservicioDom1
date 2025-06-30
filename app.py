from flask import Flask, request, jsonify
import requests
from config import Config
from models import mongo, guardar_recluso
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
mongo.init_app(app)

# Función para validar los datos (solicitar al microservicio de validación)
def validar_datos(data):
    try:
        # Enviar los datos al microservicio de validación (puedes ajustar la URL según tu configuración)
        response = requests.post("http://localhost:5001/api/validar_recluso", json=data)
        
        if response.status_code == 200:
            return True, "Datos validados correctamente"
        else:
            return False, response.json().get("error", "Error de validación desconocido")
    except Exception as e:
        return False, f"Error al conectar con el microservicio de validación: {str(e)}"


def cargar_familiares_en_otro_servicio(familiares):
    try:
        # Cambia la IP si subes a EC2 luego
        url = "http://localhost:3001/api/familiares/cargar"
        payload = {"familiares": familiares}
        response = requests.post(url, json=payload)

        if response.status_code == 200:
            print("[✓] Lista de familiares enviada al microservicio de gestión.")
        else:
            print("[!] Error al enviar familiares:", response.text)
    except Exception as e:
        print("[!] No se pudo conectar al microservicio de familiares:", str(e))

    
@app.route('/api/reclusos', methods=['POST'])
def crear_recluso():
    data = request.get_json()
    
    # Validar los datos con el microservicio de validación
    es_valido, mensaje = validar_datos(data)
    
    if not es_valido:
        return jsonify({"error": mensaje}), 400

    #NUEVO: Si hay familiares, mándalos al microservicio de gestión
    if "familiares" in data and isinstance(data["familiares"], list):
        cargar_familiares_en_otro_servicio(data["familiares"])
    
    # Si los datos son válidos, guardamos los datos en la base de datos
    recluso_id = guardar_recluso(data)

    return jsonify({"mensaje": "Recluso creado", "id": recluso_id}), 201


@app.route('/api/reclusos/<cedula>', methods=['GET'])
def obtener_recluso_por_cedula(cedula):
    try:
        recluso = mongo.db.reclusos.find_one({"id_cedula": cedula})
        if recluso:
            recluso['_id'] = str(recluso['_id'])  # Convertir ObjectId a string
            return jsonify(recluso), 200
        else:
            return jsonify({"error": "Recluso no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": f"Error al buscar el recluso: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)  # El microservicio de Ingesta corre en el puerto 5000
