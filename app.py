from flask import Flask, request, jsonify
import jwt
import datetime
import os

app = Flask(__name__)

# Clave secreta para firmar el JWT
SECRET_KEY = "supersecretkey"

# API Key requerida
API_KEY = "2f5ae96c-b558-4c7b-a590-a501ae1c3f6c"

# Lista para almacenar JWTs generados y usados
used_tokens = set()

# Obtener el entorno desde la variable de entorno (dev, qa, prod)
ENV = os.getenv('ENV', 'dev')  # Default to dev if no ENV is set

def generate_jwt():
    """Genera un JWT único con expiración de 5 minutos"""
    payload = {
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        "iat": datetime.datetime.utcnow(),
        "sub": "transaction"
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    used_tokens.add(token)  # Se almacena para verificar su uso
    return token

@app.route('/')
def root():
    """Ruta raíz dependiendo del entorno"""
    if ENV == 'dev':
        return jsonify({"message": "Welcome to the Dev environment!"}), 200
    elif ENV == 'qa':
        return jsonify({"message": "Welcome to the QA environment!"}), 200
    elif ENV == 'prod':
        return jsonify({"message": "Welcome to the Production environment!"}), 200
    else:
        return jsonify({"error": "Unknown environment"}), 400

@app.route('/generate-jwt', methods=['GET'])
def jwt_endpoint():
    """Endpoint para generar un JWT"""
    jwt_token = generate_jwt()
    return jsonify({"jwt": jwt_token})

@app.route('/DevOps', methods=['POST'])
def devops():
    # Validar API Key
    api_key = request.headers.get("X-Parse-REST-API-Key")
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # Validar JWT en los headers
    jwt_token = request.headers.get("X-JWT-KWY")
    if not jwt_token:
        return jsonify({"error": "JWT missing"}), 401

    # Verificar si el JWT fue generado pero no reutilizado
    if jwt_token not in used_tokens:
        return jsonify({"error": "Invalid or reused JWT"}), 401
    
    # Remover el JWT de la lista para que no pueda reutilizarse
    used_tokens.remove(jwt_token)

    # Decodificar y verificar JWT
    try:
        jwt.decode(jwt_token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "JWT expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid JWT"}), 401

    # Validar JSON recibido
    data = request.get_json()
    if not data or "message" not in data or "to" not in data or "from" not in data or "timeToLifeSec" not in data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    # Responder con el mensaje esperado
    response = {
        "message": f"Hello {data['to']} your message will be sent"
    }
    return jsonify(response), 200

@app.route('/DevOps', methods=['GET', 'PUT', 'DELETE'])
def method_not_allowed():
    return jsonify({"error": "ERROR"}), 405

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
