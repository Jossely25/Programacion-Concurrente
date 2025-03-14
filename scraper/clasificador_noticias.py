import schedule
import time
import logging
from pymongo import MongoClient, UpdateOne
from concurrent.futures import ThreadPoolExecutor
from transformers import pipeline 

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

try:
    client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
    db = client.noticias
    collection = db.articles
    client.server_info()  
except Exception as e:
    logging.error(f"❌ Error conectando a MongoDB: {e}")
    exit(1)

from transformers import pipeline
from pymongo import UpdateOne
import logging

try:
    modelo = pipeline("zero-shot-classification", model="joeddav/xlm-roberta-large-xnli", device=0)
except Exception as e:
    logging.error(f"❌ Error cargando modelo de IA: {e}")
    exit(1)

CATEGORIAS = ["Política", "Economía", "Deportes", "Tecnología", "Opinión"]

def clasificar_noticia(noticia):
    """Clasifica una noticia en una de las categorías usando IA."""
    try:
        titulo = noticia["titulo"]
        resultado = modelo(titulo, CATEGORIAS, multi_label=False)  # Solo una categoría
        categoria = resultado["labels"][0]  
        return UpdateOne({"_id": noticia["_id"]}, {"$set": {"categoria": categoria}})
    except Exception as e:
        logging.error(f"⚠️ Error clasificando noticia '{noticia['titulo']}': {e}")
        return None


def procesar_clasificacion():
    """Busca noticias sin clasificar y las procesa en paralelo."""
    noticias_sin_clasificar = list(collection.find({"categoria": {"$exists": False}}))
    
    if not noticias_sin_clasificar:
        logging.info("🔹 No hay noticias pendientes de clasificación.")
        return
    
    num_hilos = min(4, len(noticias_sin_clasificar))  
    logging.info(f"🚀 Clasificando {len(noticias_sin_clasificar)} noticias con {num_hilos} hilos...")

    with ThreadPoolExecutor(max_workers=num_hilos) as executor:
        operaciones = list(executor.map(clasificar_noticia, noticias_sin_clasificar))

    operaciones_validas = [op for op in operaciones if op is not None]
    if operaciones_validas:
        collection.bulk_write(operaciones_validas)
        logging.info(f"✅ {len(operaciones_validas)} noticias clasificadas y guardadas en MongoDB.")
    else:
        logging.warning("⚠️ No se realizaron actualizaciones.")

procesar_clasificacion()

schedule.every(15).minutes.do(procesar_clasificacion)

logging.info("⏳ Servicio de clasificación iniciado...")
while True:
    schedule.run_pending()
    time.sleep(60)
