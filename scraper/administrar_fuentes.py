import json
import os
import logging
from langdetect import detect

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

RUTA_JSON = "data/anexo1.json"

IDIOMAS_PERMITIDOS = ["en", "es", "fr"]

def detectar_idioma(texto):
    """Detecta el idioma del nombre de la fuente RSS."""
    try:
        idioma = detect(texto)
        if idioma in IDIOMAS_PERMITIDOS:
            return idioma
    except Exception as e:
        logging.error(f"Error al detectar idioma: {e}")
    return None

def cargar_fuentes_rss():
    """Carga las fuentes RSS desde un archivo JSON y valida su estructura."""
    if not os.path.exists(RUTA_JSON):
        logging.error(f"El archivo {RUTA_JSON} no existe.")
        raise FileNotFoundError(f"El archivo {RUTA_JSON} no existe.")

    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
            fuentes = json.load(archivo)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logging.error(f"Error al cargar el archivo JSON: {e}")
        raise ValueError(f"Error al cargar el archivo JSON: {e}")

    fuentes_validas = []
    for fuente in fuentes:
        if "nombre_fuente_rss" in fuente and "url_rss" in fuente:
            idioma = detectar_idioma(fuente["nombre_fuente_rss"])
            if idioma:
                fuentes_validas.append({**fuente, "idioma": idioma})
            else:
                logging.warning(f"Fuente excluida por idioma no permitido o no detectable: {fuente['nombre_fuente_rss']}")
        else:
            logging.warning(f"Fuente excluida por falta de datos requeridos: {fuente}")

    if not fuentes_validas:
        logging.warning("No hay fuentes válidas en el archivo JSON.")
        raise ValueError("No hay fuentes válidas en el archivo JSON.")

    return fuentes_validas

def recargar_fuentes():
    """Recarga las fuentes RSS desde el JSON en tiempo de ejecución."""
    global fuentes
    try:
        fuentes = cargar_fuentes_rss()
        logging.info(f"Fuentes RSS recargadas: {len(fuentes)} fuentes válidas.")
    except Exception as e:
        logging.error(f"Error al recargar fuentes: {e}")

if __name__ == "__main__":
    try:
        fuentes = cargar_fuentes_rss()
        logging.info(f"{len(fuentes)} fuentes RSS cargadas correctamente.")
    except Exception as e:
        logging.error(f"Error al cargar fuentes: {e}")

    while True:
        comando = input("\n🔄 Escribe 'recargar' para actualizar las fuentes o 'salir' para terminar: ").strip().lower()
        
        if comando == "recargar":
            recargar_fuentes()
        elif comando == "salir":
            logging.info("Saliendo del programa...")
            break  # Termina el bucle
        else:
            logging.warning("Comando no reconocido. Usa 'recargar' o 'salir'.")

