from flask import Flask, render_template, jsonify

app = Flask(__name__)

produtos = [
    {
        "id": "morango",
        "nome": "Cupcake de Morango",
        "descricao": "Massa de morango com cobertura de chantilly.",
        "preco": 8.00
    },
    {
        "id": "chocolate",
        "nome": "Cupcake de Chocolate",
        "descricao": "Massa de chocolate com cobertura de brigadeiro.",
        "preco": 10.00
    }
]

@app.get("/")
def inicio():
    return render_template("index.html")

@app.get("/api/produtos")
def listar_produtos():
    return jsonify(produtos)