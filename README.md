# Loja de Cupcakes

Projeto acadêmico desenvolvido para a disciplina Projeto Integrador
Transdisciplinar em Engenharia de Software II.

A aplicação simula uma loja virtual de cupcakes. O cliente consulta o
catálogo, monta um carrinho, informa dados de entrega e finaliza um pedido
com pagamento simulado. O administrador consulta os pedidos registrados e
atualiza seus status.

## Funcionalidades

### Cliente

- Visualização de cupcakes disponíveis.
- Catálogo com seis sabores, imagens e preços.
- Adição, remoção e esvaziamento do carrinho.
- Cálculo automático do total.
- Persistência do carrinho no navegador.
- Formulário de entrega com campos obrigatórios e validação de telefone com DDD.
- Finalização de pedido com mensagem de confirmação, limpeza do carrinho e do formulário.
- Registro dos pedidos em banco de dados SQLite.
- Interface responsiva para celular e computador.

### Administração

- Consulta dos pedidos registrados.
- Visualização de cliente, endereço, itens, total e data.
- Atualização de status: Recebido, Em preparo, Saiu para entrega e Entregue.
- Resumo de pedidos por status e valores formatados em real brasileiro.

## Tecnologias utilizadas

- HTML
- CSS
- JavaScript
- Python 3
- Flask
- SQLite
- Git e GitHub
- unittest

## Estrutura do projeto

```text
loja-cupcakes/
├── docs/
├── instance/
├── static/
│   ├── images/
│   ├── script.js
│   └── style.css
├── templates/
│   ├── admin_pedidos.html
│   └── index.html
├── app.py
├── requirements.txt
└── test_app.py
```

## Como executar

### 1. Criar e ativar o ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar as dependências

```powershell
python -m pip install -r requirements.txt
```

### 3. Iniciar a aplicação

```powershell
python -m flask --app app run --host 127.0.0.1 --port 5000
```

### 4. Abrir no navegador

Loja do cliente:

```text
http://127.0.0.1:5000
```

Painel administrativo:

```text
http://127.0.0.1:5000/admin/pedidos
```

## Testes

Para executar os testes automatizados:

```powershell
python -m unittest -v
```

Os testes verificam consulta do catálogo, criação de pedido, rejeição de
pedido sem itens e atualização de status.

A documentação detalhada está em:

- `docs/testes.md`
- `docs/formulario-avaliacao.md`

## Limitações da versão acadêmica

- O pagamento é apenas uma simulação.
- O painel administrativo não possui autenticação.
- A aplicação foi criada para fins educacionais e de demonstração.
