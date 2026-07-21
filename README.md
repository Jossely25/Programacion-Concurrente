# Concurrent News Scraper 📰

Aplicación desarrollada como proyecto de Programación Concurrente para la recopilación, clasificación y visualización de noticias obtenidas mediante fuentes RSS. El sistema automatiza la extracción de información, organiza las noticias por categorías y las presenta a través de una interfaz web.

## Características

- Extracción automática de noticias desde fuentes RSS.
- Clasificación de noticias por categorías.
- Procesamiento de datos en formato JSON.
- Interfaz web para visualizar la información recopilada.
- Arquitectura modular que separa el scraper, el clasificador y el backend.
- Fácil incorporación de nuevas fuentes RSS.

---

## Tecnologías utilizadas

- Python
- Flask
- HTML5
- RSS Feed
- JSON

---

## Estructura del proyecto

```text
concurrent-news-scraper/
│
├── backend/
│   ├── app.py
│   └── templates/
│       └── index.html
│
├── scraper/
│   ├── scraper_rss.py
│   ├── clasificador_noticias.py
│   ├── administrar_fuentes.py
│   └── data/
│       └── anexo1.json
│
└── README.md
```

---

## Funcionalidades

### Scraper RSS

- Consulta diferentes fuentes RSS.
- Descarga las noticias disponibles.
- Procesa la información obtenida.

### Clasificador

- Analiza el contenido de las noticias.
- Organiza las noticias según la categoría correspondiente.
- Genera la información que posteriormente consume la interfaz web.

### Backend

- Expone la información procesada mediante una aplicación Flask.
- Renderiza la interfaz para visualizar las noticias clasificadas.

---

## Requisitos

- Python 3.10 o superior.
- pip.

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/USUARIO/concurrent-news-scraper.git
```

### 2. Instalar dependencias

```bash
pip install flask feedparser beautifulsoup4 requests
```

---

## Ejecución

### Paso 1: Obtener las noticias

```bash
python scraper/scraper_rss.py
```

### Paso 2: Clasificar las noticias

```bash
python scraper/clasificador_noticias.py
```

### Paso 3: Ejecutar la aplicación web

```bash
cd backend

python app.py
```

La aplicación estará disponible en:

```text
http://localhost:5000
```

---

## Flujo de funcionamiento

1. Se consultan las fuentes RSS configuradas.
2. El scraper descarga las noticias disponibles.
3. Las noticias son almacenadas en formato JSON.
4. El clasificador organiza el contenido por categorías.
5. El backend Flask presenta la información mediante una interfaz web.

---

## Organización del proyecto

| Carpeta | Descripción |
|---------|-------------|
| `backend/` | Aplicación Flask encargada de mostrar la información. |
| `templates/` | Plantillas HTML del sistema. |
| `scraper/` | Scripts para extracción y clasificación de noticias. |
| `data/` | Archivos JSON con la información procesada. |

---

## Despliegue

El proyecto puede ejecutarse en cualquier entorno compatible con Python y Flask, ya sea de forma local o en un servidor Linux.

---

## Capturas

Puedes agregar imágenes como:

```text
docs/home.png

docs/noticias.png

docs/categorias.png
```

---

## Autor

Desarrollado por **Jossely Elena Aguirre Acuña**.

---

## Licencia

Proyecto desarrollado con fines académicos para la asignatura de **Programación Concurrente**.
