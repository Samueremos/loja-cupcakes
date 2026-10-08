const produtos = [
    {
        nome: "Cupcake de Morango",
        descricao: "Massa de morango com cobertura de chantilly.",
        preco: 8.00,
        quantidade: 0
    },
    {
        nome: "Cupcake de Chocolate",
        descricao: "Massa de chocolate com cobertura de brigadeiro.",
        preco: 10.00,
        quantidade: 0
    }
];

function formatarMoeda(valor) {
    return valor.toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
}

function mostrarProdutos() {
    const vitrine = document.getElementById("vitrine");
    vitrine.textContent = "";

    for (const item of produtos) {
        const cartao = document.createElement("article");

        const nome = document.createElement("h2");
        nome.textContent = item.nome;

        const descricao = document.createElement("p");
        descricao.textContent = item.descricao;

        const preco = document.createElement("p");
        preco.textContent = "Preço: " + formatarMoeda(item.preco);

        const botao = document.createElement("button");
        botao.textContent = "Adicionar ao carrinho";

        botao.addEventListener("click", function () {
            adicionarAoCarrinho(item);
        });

        cartao.append(nome, descricao, preco, botao);
        vitrine.append(cartao);
    }
}

function adicionarAoCarrinho(item) {
    item.quantidade = item.quantidade + 1;
    atualizarCarrinho();
}

function removerDoCarrinho(item) {
    if (item.quantidade > 0) {
        item.quantidade = item.quantidade - 1;
        atualizarCarrinho();
    }
}

function atualizarCarrinho() {
    const lista = document.getElementById("itens-carrinho");
    lista.textContent = "";

    let quantidadeTotal = 0;
    let valorTotal = 0;

    for (const item of produtos) {
        quantidadeTotal = quantidadeTotal + item.quantidade;
        valorTotal = valorTotal + item.quantidade * item.preco;

        if (item.quantidade > 0) {
            const linha = document.createElement("article");

            const resumo = document.createElement("p");
            const subtotal = item.quantidade * item.preco;

            resumo.textContent =
                item.nome + " — Quantidade: " + item.quantidade +
                " — Subtotal: " + formatarMoeda(subtotal);

            const botaoRemover = document.createElement("button");
            botaoRemover.textContent = "Remover uma unidade";

            botaoRemover.addEventListener("click", function () {
                removerDoCarrinho(item);
            });

            linha.append(resumo, botaoRemover);
            lista.append(linha);
        }
    }

    if (quantidadeTotal === 0) {
        lista.textContent = "Seu carrinho está vazio.";
    }

    document.getElementById("carrinho").textContent =
        "Itens no carrinho: " + quantidadeTotal;

    document.getElementById("total").textContent =
        "Total: " + formatarMoeda(valorTotal);

    document.getElementById("botao-esvaziar").disabled =
        quantidadeTotal === 0;
}

function esvaziarCarrinho() {
    for (const item of produtos) {
        item.quantidade = 0;
    }

    atualizarCarrinho();
}

mostrarProdutos();
atualizarCarrinho();