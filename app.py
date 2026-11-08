from contextlib import contextmanager

import sqlite3
from pathlib import Path

from flask import (
    Flask, abort, jsonify, redirect, render_template, request, url_for
)

app = Flask(__name__)

CAMINHO_BANCO = Path(app.instance_path) / "loja_cupcakes.db"

@contextmanager
def obter_conexao():
    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row

    try:
        yield conexao
        conexao.commit()
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()

def criar_banco():
    Path(app.instance_path).mkdir(exist_ok=True)

    with obter_conexao() as conexao:
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_cliente TEXT NOT NULL,
                telefone TEXT NOT NULL,
                endereco TEXT NOT NULL,
                valor_total REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'Recebido',
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conexao.execute("""
            CREATE TABLE IF NOT EXISTS itens_pedido (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pedido_id INTEGER NOT NULL,
                produto_id TEXT NOT NULL,
                nome_produto TEXT NOT NULL,
                preco_unitario REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
            )
        """)

criar_banco()

produtos = [
    {
        "id": "morango",
        "nome": "Cupcake de Morango",
        "descricao": "Massa de morango com cobertura de chantilly.",
        "preco": 8.00,
        "imagem": "images/cupcake-morango.png"
    },
    {
        "id": "chocolate",
        "nome": "Cupcake de Chocolate",
        "descricao": "Massa de chocolate com cobertura de brigadeiro.",
        "preco": 10.00,
        "imagem": "images/cupcake-chocolate.png"
    },
    {
        "id": "baunilha",
        "nome": "Cupcake de Baunilha",
        "descricao": "Massa de baunilha com cobertura cremosa e confeitos coloridos.",
        "preco": 8.50,
        "imagem": "images/cupcake-baunilha.png"
    },
    {
        "id": "red-velvet",
        "nome": "Cupcake Red Velvet",
        "descricao": "Massa red velvet com cobertura de cream cheese e farofa vermelha.",
        "preco": 11.00,
        "imagem": "images/cupcake-red-velvet.png"
    },
    {
        "id": "limao",
        "nome": "Cupcake de Limão",
        "descricao": "Massa de limão com cobertura cítrica e raspas de limão.",
        "preco": 9.50,
        "imagem": "images/cupcake-limao.png"
    },
    {
        "id": "cookies-cream",
        "nome": "Cupcake Cookies & Cream",
        "descricao": "Massa de chocolate com cobertura de biscoito e creme.",
        "preco": 11.50,
        "imagem": "images/cupcake-cookies-cream.png"
    }
]

@app.get("/")
def inicio():
    return render_template("index.html")

@app.get("/api/produtos")
def listar_produtos():
    return jsonify(produtos)

@app.post("/api/pedidos")
def criar_pedido():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie os dados do pedido em JSON."}), 400

    nome = str(dados.get("nome", "")).strip()
    telefone = str(dados.get("telefone", "")).strip()
    endereco = str(dados.get("endereco", "")).strip()
    itens_recebidos = dados.get("itens")

    if not nome or not telefone or not endereco:
        return jsonify({
            "erro": "Nome, telefone e endereço são obrigatórios."
        }), 400

    if not isinstance(itens_recebidos, list) or not itens_recebidos:
        return jsonify({
            "erro": "Adicione pelo menos um cupcake ao pedido."
        }), 400

    produtos_por_id = {produto["id"]: produto for produto in produtos}
    itens_validos = []
    valor_total = 0

    for item_recebido in itens_recebidos:
        if not isinstance(item_recebido, dict):
            return jsonify({"erro": "Item de pedido inválido."}), 400

        produto_id = item_recebido.get("produto_id")
        quantidade = item_recebido.get("quantidade")

        if (
            produto_id not in produtos_por_id
            or not isinstance(quantidade, int)
            or quantidade <= 0
        ):
            return jsonify({"erro": "Produto ou quantidade inválidos."}), 400

        produto = produtos_por_id[produto_id]
        valor_total += produto["preco"] * quantidade

        itens_validos.append({
            "produto_id": produto["id"],
            "nome_produto": produto["nome"],
            "preco_unitario": produto["preco"],
            "quantidade": quantidade
        })

    with obter_conexao() as conexao:
        cursor = conexao.execute("""
            INSERT INTO pedidos (
                nome_cliente, telefone, endereco, valor_total
            )
            VALUES (?, ?, ?, ?)
        """, (nome, telefone, endereco, valor_total))

        pedido_id = cursor.lastrowid

        for item in itens_validos:
            conexao.execute("""
                INSERT INTO itens_pedido (
                    pedido_id, produto_id, nome_produto,
                    preco_unitario, quantidade
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                pedido_id,
                item["produto_id"],
                item["nome_produto"],
                item["preco_unitario"],
                item["quantidade"]
            ))

    return jsonify({
        "mensagem": "Pedido registrado com sucesso.",
        "pedido_id": pedido_id,
        "status": "Recebido",
        "valor_total": valor_total
    }), 201

STATUS_PERMITIDOS = [
    "Recebido",
    "Em preparo",
    "Saiu para entrega",
    "Entregue"
]


@app.get("/admin/pedidos")
def admin_pedidos():
    with obter_conexao() as conexao:
        pedidos = conexao.execute("""
            SELECT
                pedidos.id,
                pedidos.nome_cliente,
                pedidos.telefone,
                pedidos.endereco,
                pedidos.valor_total,
                pedidos.status,
                pedidos.criado_em,
                GROUP_CONCAT(
                    itens_pedido.nome_produto || ' x' ||
                    itens_pedido.quantidade,
                    ', '
                ) AS itens
            FROM pedidos
            LEFT JOIN itens_pedido
                ON itens_pedido.pedido_id = pedidos.id
            GROUP BY pedidos.id
            ORDER BY pedidos.id DESC
        """).fetchall()

    return render_template(
        "admin_pedidos.html",
        pedidos=pedidos,
        status_permitidos=STATUS_PERMITIDOS
    )


@app.post("/admin/pedidos/<int:pedido_id>/status")
def atualizar_status_pedido(pedido_id):
    novo_status = request.form.get("status", "")

    if novo_status not in STATUS_PERMITIDOS:
        abort(400, "Status inválido.")

    with obter_conexao() as conexao:
        cursor = conexao.execute("""
            UPDATE pedidos
            SET status = ?
            WHERE id = ?
        """, (novo_status, pedido_id))

        if cursor.rowcount == 0:
            abort(404, "Pedido não encontrado.")

    return redirect(url_for("admin_pedidos"))
