# Testes da Solução

## Projeto

Loja de Cupcakes - Projeto Integrador Transdisciplinar em Engenharia de Software II.

## Objetivo dos testes

Verificar se o sistema permite consultar o catálogo, montar um pedido,
registrar os dados no banco SQLite e atualizar o status do pedido no
painel administrativo.

## Ambiente de teste

- Sistema operacional: Windows 11
- Linguagem do back-end: Python 3.14
- Framework: Flask 3.1.3
- Banco de dados: SQLite
- Front-end: HTML, CSS e JavaScript
- Navegador utilizado: navegador moderno compatível com JavaScript

## Testes automatizados

Os testes automatizados estão no arquivo `test_app.py` e usam um banco
temporário, sem modificar os pedidos criados durante o uso da aplicação.

| ID | Teste | Resultado esperado | Resultado obtido |
|---|---|---|---|
| TA-01 | Consultar catálogo | A API retorna os seis cupcakes cadastrados, com imagem e preço. | Aprovado |
| TA-02 | Criar pedido válido | O pedido é registrado com status Recebido e total correto. | Aprovado |
| TA-03 | Criar pedido sem itens | O sistema rejeita o pedido e informa o erro. | Aprovado |
| TA-04 | Atualizar status | O administrador altera o pedido para Em preparo. | Aprovado |
| TA-05 | Validar telefone | O sistema rejeita telefone sem DDD válido. | Aprovado |
| TA-06 | Painel administrativo | O painel exibe resumo dos status e valor em formato brasileiro. | Aprovado |
| TA-07 | Página inicial | A loja exibe as seções de catálogo, carrinho e dados de entrega. | Aprovado |

Comando executado:

    python -m unittest -v

Resultado observado:

    Ran 7 tests
    OK

## Testes manuais

| ID | Cenário | Passos | Resultado esperado | Resultado obtido |
|---|---|---|---|---|
| TM-01 | Adicionar produtos | Adicionar 2 cupcakes de morango e 1 de chocolate. | Carrinho apresenta 3 itens e total de R$ 26,00. | Aprovado |
| TM-02 | Remover produto | Remover uma unidade de morango do carrinho. | Quantidade e valor total são recalculados. | Aprovado |
| TM-03 | Persistir carrinho | Adicionar produtos e atualizar a página. | Itens do carrinho permanecem armazenados no navegador. | Aprovado |
| TM-04 | Validar formulário | Tentar finalizar sem preencher os campos obrigatórios. | O navegador solicita o preenchimento dos campos. | Aprovado |
| TM-05 | Finalizar pedido | Preencher dados fictícios e finalizar um pedido. | Pedido recebe número, status Recebido e é salvo no SQLite. | Aprovado |
| TM-06 | Administrar pedido | Abrir o painel administrativo e mudar o status. | Status atualizado é mantido após recarregar a página. | Aprovado |

## Conclusão

Os testes automatizados e manuais demonstraram que as principais
funcionalidades da solução estão operando: catálogo, carrinho,
formulário de entrega, registro de pedidos, persistência no banco de
dados e atualização do status administrativo.
