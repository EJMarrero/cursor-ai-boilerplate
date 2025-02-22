import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env (si fuese necesario para otras configuraciones)
load_dotenv()

def scrape_twitter_trending(url="https://trends24.in/"):
    """
    Realiza web scraping en Trends24 para obtener los trending topics de Twitter/X,
    extrayendo tanto el texto del topic como el href de cada enlace.

    La estructura que se maneja es la siguiente:
    <ol class="trend-card__list">
      <li>
        <span class="trend-name">
          <a href="URL_DEL_TOPIC" class="trend-link">Texto_del_Topic</a>
          <span class="tweet-count" data-count="..."></span>
        </span>
      </li>
      ...
    </ol>

    Retorna una lista de diccionarios con la siguiente estructura:
      [
         {
             "topic": "Texto del topic",
             "url": "URL extraído del atributo href"
         },
         ...
      ]
    """
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/91.0.4472.124 Safari/537.36"),
        "Referer": "https://trends24.in/"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al acceder a la URL {url}: {e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    trending_topics = []
    # Buscar el contenedor <ol> que contiene la lista de tópicos
    lista = soup.find("ol", class_="trend-card__list")
    if not lista:
        print("No se encontró la lista de trending topics.")
        return trending_topics

    # Iterar sobre cada elemento <li> de la lista
    items = lista.find_all("li")
    for item in items:
        # Aquí se utiliza find para extraer el primer <a> con el atributo href dentro del <li>
        a_tag = item.find("a", href=True)
        if a_tag:
            topic_text = a_tag.get_text(strip=True)
            link_href = a_tag.get("href")  # Obtiene el valor del atributo href
            trending_topics.append({"topic": topic_text, "url": link_href})
    
    return trending_topics

def main():
    topics = scrape_twitter_trending()
    if topics:
        for topic in topics:
            print(f"Topic: {topic['topic']}")
            print(f"URL: {topic['url']}")
            print("-" * 40)
    else:
        print("No se pudieron extraer trending topics.")

if __name__ == "__main__":
    main() 