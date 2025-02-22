# Análisis de Sentimientos – Plataforma Completa

Este proyecto integra varias funcionalidades en una única plataforma que permite:

- **Recolectar opiniones y trending topics:**  
  Se realiza web scraping de fuentes públicas (por ejemplo, *quotes.toscrape.com* para opiniones y *Trends24* para trending topics).

- **Preprocesar y analizar las opiniones:**  
  Se limpia el contenido HTML, se normaliza el texto y se realiza un análisis de sentimientos, temas y categorías mediante la API de OpenAI.

- **Almacenar la información:**  
  Las opiniones originales y sus análisis se guardan en una base de datos SQLite.

- **Exponer los datos mediante una API REST:**  
  Se desarrolló un backend con Flask que expone endpoints para obtener tanto las opiniones analizadas como los trending topics.

- **Interfaz de usuario moderna:**  
  Se utiliza Vue 3 con Pinia y TailwindCSS para construir un frontend que consume la API y permite visualizar la información de forma interactiva.

- **Pruebas end-to-end con Cypress:**  
  Se incluye una configuración de Cypress para realizar pruebas sobre la experiencia de usuario.

---

## Tabla de Contenidos

- **Características**
- **Tecnologías**
- **Configuración técnica**
  - Requisitos
  - Instalación de dependencias
  - Configuración de variables de entorno
- **Ejecución del Backend y Pipeline de Análisis**
- **Ejecución del Frontend**
- **Pruebas End-to-End con Cypress**
- **Arquitectura y Detalles Técnicos**
- **Guía de Usuario**
- **Futuras Mejoras**

---

## Características

- **Web Scraping:**
  - Obtención de opiniones (como ejemplo se usa *quotes.toscrape.com*).
  - Scraping de trending topics desde *Trends24* (utilizando Requests y BeautifulSoup).

- **Preprocesamiento y Análisis:**
  - Limpieza del HTML para extraer el contenido en texto.
  - Conversión a minúsculas y eliminación de caracteres especiales.
  - Análisis de sentimiento, detección de temas y clasificación mediante un LLM (con la API de OpenAI).

- **Almacenamiento:**
  - Persistencia de la opinión original y del análisis en una base de datos SQLite (tabla `reviews`).

- **API REST:**
  - Endpoint raíz con mensaje de bienvenida.
  - `GET /api/opiniones` para obtener las opiniones analizadas.
  - `GET /api/trending` para obtener los trending topics.

- **Frontend:**
  - Interfaz construida en Vue 3.
  - Gestión de estado global con Pinia.
  - Estilos modernos con TailwindCSS.
  - Navegación por pestañas para visualizar "Opiniones Analizadas" y "Trending Topics".
  - Componentes reutilizables: `ReviewCard` para opiniones y `TrendingCard` para trending topics.

- **Pruebas:**
  - Configuración y ejemplos de pruebas end-to-end (E2E) utilizando Cypress.

---

## Tecnologías

- **Backend:** Python, Flask, SQLite, Requests, BeautifulSoup, OpenAI API, dotenv.
- **Scraping y Análisis:** Módulos personalizados en Python para scraping y análisis.
- **Frontend:** Vue 3, Pinia, Vite, TailwindCSS.
- **Testing:** Cypress (E2E).
- **Gestión de Variables de Entorno:** Archivo `.env`.

---

## Configuración Técnica

### Requisitos

- Python 3.7+
- Node.js 14+
- Git

### Instalación de Dependencias

#### Backend

Navega al directorio del backend (o la raíz del proyecto) y crea un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt

