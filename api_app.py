from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from dotenv import load_dotenv
from twitter_trends_scraper import scrape_twitter_trending  # Importa la función para obtener trending topics

# Cargar variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
# Habilitar CORS globalmente para toda la aplicación (esto permite cualquier origen en desarrollo)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=False)

def get_all_reviews(db_path="opiniones.db"):
    """
    Consulta todas las opiniones analizadas almacenadas en la base de datos.
    Retorna una lista de diccionarios con los campos:
       - id
       - opinion_original
       - opinion_limpia
       - sentimiento
       - temas
       - categoria
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT id, opinion_original, opinion_limpia, sentimiento, temas, categoria FROM reviews")
    rows = cursor.fetchall()
    conn.close()
    
    resultados = []
    for row in rows:
        review = {
            "id": row[0],
            "opinion_original": row[1],
            "opinion_limpia": row[2],
            "sentimiento": row[3],
            "temas": row[4],
            "categoria": row[5]
        }
        resultados.append(review)
    return resultados

@app.route("/")
def index():
    """
    Endpoint raíz que muestra un mensaje de bienvenida.
    """
    mensaje = (
        "Bienvenido a la API de Opiniones y Trending Topics.<br>"
        "Utilice /api/opiniones para obtener las opiniones analizadas.<br>"
        "Utilice /api/trending para obtener los trending topics de Twitter/X."
    )
    return mensaje

@app.route("/api/opiniones", methods=["GET"])
def api_opiniones():
    try:
        reviews = get_all_reviews()
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener opiniones: {str(e)}"}), 500

@app.route("/api/trending", methods=["GET"])
def api_trending():
    try:
        trending_topics = scrape_twitter_trending()
        return jsonify(trending_topics), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener trending topics: {str(e)}"}), 500

if __name__ == "__main__":
    # Iniciar el servidor Flask en modo debug en el puerto 8000
    app.run(debug=True, host="0.0.0.0", port=8000) 