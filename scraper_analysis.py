import os
import re
import time
import json
import sqlite3
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def scrape_reviews(url):
    """
    Realiza la petición HTTP a la URL y extrae las opiniones.
    
    Si se utiliza la URL de prueba "http://quotes.toscrape.com/", se buscan
    los elementos <div class="quote">. En caso de utilizar otra fuente, modifica
    el selector para adaptarlo a la estructura HTML de la página.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza excepción si ocurre algún error HTTP
    except requests.RequestException as e:
        print(f"Error al obtener la página: {e}")
        return []
    
    # Parsear el HTML
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Seleccionar el grupo de elementos dependiendo de la URL
    if "quotes.toscrape.com" in url:
        review_elements = soup.find_all("div", class_="quote")
    else:
        review_elements = soup.find_all("div", class_="review-content")
        
    reviews = []
    for element in review_elements:
        # Se guarda el HTML completo del elemento. Puedes también extraer solo el texto.
        reviews.append(str(element))
    
    if not reviews:
        print("No se encontraron opiniones en la página.")
    return reviews

def clean_text(raw_html):
    """
    Limpia el texto eliminando etiquetas HTML, convierte a minúsculas y elimina caracteres especiales.
    Se conservan letras (incluyendo acentuadas), números y espacios.
    """
    # Eliminar etiquetas HTML
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ")
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar caracteres especiales (se conservan letras, números y espacios)
    text = re.sub(r'[^a-záéíóúñ0-9\s]', '', text)
    # Reducir múltiples espacios a uno solo
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def analyze_review(text):
    """
    Utiliza la API de OpenAI para analizar el sentimiento del texto.
    Se solicita: sentimiento predominante (positivo, negativo o neutro),
    temas relevantes y una categoría general.
    
    El prompt se estructura para que la respuesta esté en formato JSON con las claves:
    "sentimiento", "temas" (lista de temas) y "categoria".
    """
    prompt = f"""
    Realiza un análisis del siguiente texto: "{text}".
    Indica el sentimiento predominante (positivo, negativo o neutro), los temas relevantes que se abordan y una categoría general a la que pertenece la opinión.
    Responde en formato JSON con las claves "sentimiento", "temas" (lista de temas) y "categoria".
    """
    try:
        # Se utiliza la API de chat de OpenAI (por ejemplo, GPT-3.5-turbo)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un analista de opiniones."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        resultado_text = response.choices[0].message['content'].strip()
        # Intentar parsear el resultado como JSON
        analysis = json.loads(resultado_text)
        return analysis
    except Exception as e:
        print(f"Error al analizar la opinión: {e}")
        return {}

def init_db(db_path="opiniones.db"):
    """
    Inicializa la base de datos SQLite y crea la tabla 'reviews' si esta no existe.
    La tabla contiene:
       - id: Identificador único.
       - opinion_original: Texto original (HTML) de la opinión.
       - opinion_limpia: Texto preprocesado.
       - sentimiento: Resultado del análisis de sentimiento.
       - temas: Lista de temas en formato JSON.
       - categoria: Categoría general asignada.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            opinion_original TEXT,
            opinion_limpia TEXT,
            sentimiento TEXT,
            temas TEXT,
            categoria TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_review(opinion_original, opinion_limpia, analysis, db_path="opiniones.db"):
    """
    Guarda la opinión y su análisis en la base de datos SQLite.
    Se espera que 'analysis' sea un diccionario con las claves: 'sentimiento', 'temas' y 'categoria'.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sentimiento = analysis.get("sentimiento", "")
    temas = json.dumps(analysis.get("temas", []))  # Se almacena la lista en formato JSON
    categoria = analysis.get("categoria", "")
    cursor.execute(
        "INSERT INTO reviews (opinion_original, opinion_limpia, sentimiento, temas, categoria) VALUES (?, ?, ?, ?, ?)",
        (opinion_original, opinion_limpia, sentimiento, temas, categoria)
    )
    conn.commit()
    conn.close()

def process_reviews(url):
    """
    Flujo principal para:
       1. Realizar web scraping de las opiniones.
       2. Preprocesar el contenido de cada opinión.
       3. Analizar cada opinión usando la API de OpenAI.
       4. Guardar la opinión original y el análisis en la base de datos.
    """
    print("Iniciando el proceso de scraping...")
    reviews_html = scrape_reviews(url)
    print(f"Se encontraron {len(reviews_html)} opiniones.")
    
    # Inicializar la base de datos
    init_db()
    
    for review_html in reviews_html:
        # Preprocesar la opinión
        opinion_limpia = clean_text(review_html)
        print("Analizando opinión:", opinion_limpia)
        
        # Analizar sentimiento, temas y categoría
        analysis = analyze_review(opinion_limpia)
        print("Resultado del análisis:", analysis)
        
        # Almacenar los datos en la base de datos
        save_review(review_html, opinion_limpia, analysis)
        
        # Pequeño retardo para no saturar la API
        time.sleep(1)

def main():
    # Para probar, se usa la URL de quotes.toscrape.com que contiene "citas" como ejemplo de opiniones.
    # Si tienes una URL real con opiniones, reemplázala y ajusta el selector en la función scrape_reviews.
    url = "http://quotes.toscrape.com/"
    process_reviews(url)

if __name__ == "__main__":
    # Verificar que la variable de entorno OPENAI_API_KEY esté definida
    if "OPENAI_API_KEY" not in os.environ:
        print("Por favor, define la variable de entorno OPENAI_API_KEY en el archivo .env o en el entorno.")
        exit(1)
    openai.api_key = os.getenv("OPENAI_API_KEY")
    main() 