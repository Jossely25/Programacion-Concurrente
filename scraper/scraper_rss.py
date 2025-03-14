import feedparser   
import requests     
import schedule     
import time         
import psutil        
from bs4 import BeautifulSoup  
from pymongo import MongoClient, errors  
from concurrent.futures import ThreadPoolExecutor  
import json        
import os            
import logging       

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

RUTA_JSON = "data/anexo1.json"

def cargar_fuentes_rss():
    """Carga las fuentes RSS desde un archivo JSON y las devuelve en una lista."""
    if not os.path.exists(RUTA_JSON):
        logging.error(f"El archivo {RUTA_JSON} no existe.")
        raise FileNotFoundError(f"El archivo {RUTA_JSON} no existe.")
    
    with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
        try:
            return json.load(archivo)
        except json.JSONDecodeError:
            logging.error("El archivo JSON tiene un formato inválido.")
            raise ValueError("El archivo JSON tiene un formato inválido.")

def conectar_mongodb():
    """Intenta conectar con MongoDB y reintenta si falla."""
    for intento in range(3): 
        try:
            client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
            client.server_info()  
            logging.info("Conexión exitosa a MongoDB")
            return client
        except errors.ServerSelectionTimeoutError:
            logging.warning(f"Intento {intento + 1}: No se pudo conectar a MongoDB. Reintentando...")
            time.sleep(5)
    logging.critical("No se pudo establecer conexión con MongoDB después de 3 intentos.")
    raise Exception("No se pudo establecer conexión con MongoDB.")

client = conectar_mongodb()
db = client.noticias
collection = db.articles

def obtener_numero_hilos():
    return max(1, psutil.cpu_count(logical=True) - 1)  

def extraer_imagen(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            img_tag = soup.find("meta", property="og:image")  
            return img_tag["content"] if img_tag else None
    except requests.RequestException as e:
        logging.error(f"Error al obtener imagen de {url}: {e}")
        return None
    return None

def procesar_feed(fuente):
    logging.info(f"Procesando: {fuente['nombre_fuente_rss']}")
    try:
        feed = feedparser.parse(fuente["url_rss"])
    except Exception as e:
        logging.error(f"Error al procesar {fuente['nombre_fuente_rss']}: {e}")
        return

    for entrada in feed.entries:
        articulo = {
            "titulo": entrada.title,
            "fecha_publicacion": entrada.get("published", "Fecha no disponible"),
            "url": entrada.link,
            "imagen": extraer_imagen(entrada.link),
            "descripcion": entrada.get("summary", "No hay descripción"),
            "fuente": fuente["nombre_fuente_rss"]
        }

        collection.update_one(
            {"url": articulo["url"]},  
            {"$set": articulo},  
            upsert=True
        )
        logging.info(f"✅ Guardado: {articulo['titulo']}")

def ejecutar_scraping():
    fuentes = cargar_fuentes_rss()
    num_hilos = obtener_numero_hilos()
    logging.info(f"Ejecutando scraping con {num_hilos} hilos...")

    with ThreadPoolExecutor(max_workers=num_hilos) as executor:
        executor.map(procesar_feed, fuentes)

ejecutar_scraping()

schedule.every(10).minutes.do(ejecutar_scraping)

logging.info("⏳ Servicio de scraping iniciado...")
while True:
    schedule.run_pending()
    time.sleep(60)

