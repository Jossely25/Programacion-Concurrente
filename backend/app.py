from flask import Flask, render_template, request
from pymongo import MongoClient
import math  

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
db = client.noticias
collection = db.articles

@app.route('/')
def index():
    categoria = request.args.get('categoria', '')
    page = int(request.args.get('page', 1))
    per_page = 20
    skip = (page - 1) * per_page

    query = {}
    if categoria:
        query['categoria'] = categoria

    noticias = list(collection.find(query).sort("fecha_publicacion", -1).skip(skip).limit(per_page))
    total_noticias = collection.count_documents(query)
    total_pages = math.ceil(total_noticias / per_page)  

    return render_template("index.html", noticias=noticias, page=page, total_pages=total_pages, per_page=per_page, categoria=categoria)

if __name__ == '__main__':
    app.run(debug=True)

