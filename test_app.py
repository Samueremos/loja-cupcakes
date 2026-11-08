import tempfile
import unittest
from pathlib import Path

import app as loja


class TesteLojaCupcakes(unittest.TestCase):
    def setUp(self):
        self.pasta_temporaria = tempfile.TemporaryDirectory()

        loja.CAMINHO_BANCO = (
            Path(self.pasta_temporaria.name) / "teste_loja.db"
        )

        loja.app.config["TESTING"] = True
        loja.criar_banco()

        self.cliente = loja.app.test_client()

    def tearDown(self):
        self.pasta_temporaria.cleanup()

    def criar_dados_pedido(self):
        return {
            "nome": "Cliente de Teste",
            "telefone": "11999999999",
            "endereco": "Rua de Teste, 123, São Paulo - SP",
            "itens": [
                {
                    "produto_id": "morango",
                    "quantidade": 2
                },
                {
                    "produto_id": "chocolate",
                    "quantidade": 1
                }
            ]
        }

    def test_listar_produtos(self):
        resposta = self.cliente.get("/api/produtos")

        self.assertEqual(resposta.status_code, 200)

        produtos = resposta.get_json()

        self.assertEqual(len(produtos), 6)
        self.assertEqual(produtos[0]["id"], "morango")
        self.assertEqual(produtos[1]["preco"], 10.00)
        self.assertEqual(produtos[5]["id"], "cookies-cream")

    def test_pagina_inicial_exibe_catalogo_e_formulario(self):
        resposta = self.cliente.get("/")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("Sabores disponíveis", pagina)
        self.assertIn('id="formulario-pedido"', pagina)

    def test_criar_pedido_valido(self):
        resposta = self.cliente.post(
            "/api/pedidos",
            json=self.criar_dados_pedido()
        )

        self.assertEqual(resposta.status_code, 201)

        resultado = resposta.get_json()

        self.assertEqual(resultado["status"], "Recebido")
        self.assertEqual(resultado["valor_total"], 26.00)

        with loja.obter_conexao() as conexao:
            pedido = conexao.execute("""
                SELECT nome_cliente, valor_total, status
                FROM pedidos
            """).fetchone()

            itens = conexao.execute("""
                SELECT quantidade
                FROM itens_pedido
            """).fetchall()

        self.assertEqual(pedido["nome_cliente"], "Cliente de Teste")
        self.assertEqual(pedido["valor_total"], 26.00)
        self.assertEqual(pedido["status"], "Recebido")
        self.assertEqual(len(itens), 2)

    def test_rejeitar_pedido_sem_itens(self):
        dados = self.criar_dados_pedido()
        dados["itens"] = []

        resposta = self.cliente.post("/api/pedidos", json=dados)

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(
            resposta.get_json()["erro"],
            "Adicione pelo menos um cupcake ao pedido."
        )

    def test_rejeitar_telefone_sem_ddd_valido(self):
        dados = self.criar_dados_pedido()
        dados["telefone"] = "12345"

        resposta = self.cliente.post("/api/pedidos", json=dados)

        self.assertEqual(resposta.status_code, 400)
        self.assertEqual(
            resposta.get_json()["erro"],
            "Informe um telefone com DDD, contendo 10 ou 11 dígitos."
        )

    def test_atualizar_status_do_pedido(self):
        resposta_criacao = self.cliente.post(
            "/api/pedidos",
            json=self.criar_dados_pedido()
        )

        pedido_id = resposta_criacao.get_json()["pedido_id"]

        resposta_atualizacao = self.cliente.post(
            f"/admin/pedidos/{pedido_id}/status",
            data={"status": "Em preparo"},
            follow_redirects=True
        )

        self.assertEqual(resposta_atualizacao.status_code, 200)

        with loja.obter_conexao() as conexao:
            pedido = conexao.execute("""
                SELECT status
                FROM pedidos
                WHERE id = ?
            """, (pedido_id,)).fetchone()

        self.assertEqual(pedido["status"], "Em preparo")

    def test_painel_admin_exibe_resumo_e_moeda_brasileira(self):
        self.cliente.post("/api/pedidos", json=self.criar_dados_pedido())

        resposta = self.cliente.get("/admin/pedidos")
        pagina = resposta.get_data(as_text=True)

        self.assertEqual(resposta.status_code, 200)
        self.assertIn("R$ 26,00", pagina)
        self.assertIn("Recebido", pagina)


if __name__ == "__main__":
    unittest.main()
