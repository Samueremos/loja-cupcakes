let produtos = [];

function salvarCarrinho() {
    const quantidades = {};

    for (const item of produtos) {
        quantidades[item.id] = item.quantidade;
    }

    try {
        localStorage.setItem(
            "loja-cupcakes-carrinho",
            JSON.stringify(quantidades)
        );
    } catch (erro) {
        console.warn("Não foi possível salvar o carrinho.", erro);
    }
}

function carregarCarrinho() {
    try {
        const textoSalvo = localStorage.getItem("loja-cupcakes-carrinho");

        if (textoSalvo === null) {
            return;
        }

        const quantidades = JSON.parse(textoSalvo);

        if (quantidades === null || typeof quantidades !== "object") {
            return;
        }

        for (const item of produtos) {
            const quantidadeSalva = quantidades[item.id];

            if (Number.isSafeInteger(quantidadeSalva) && quantidadeSalva >= 0) {
                item.quantidade = quantidadeSalva;
            }
        }
    } catch (erro) {
        console.warn("Não foi possível recuperar o carrinho.", erro);
    }
}

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
    document.getElementById("mensagem-pedido").textContent = "";

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

    salvarCarrinho();
}

function esvaziarCarrinho() {
    for (const item of produtos) {
        item.quantidade = 0;
    }

    atualizarCarrinho();
}

function revisarPedido(evento) {
    evento.preventDefault();

    const mensagem = document.getElementById("mensagem-pedido");

    let quantidadeTotal = 0;
    let valorTotal = 0;

    for (const item of produtos) {
        quantidadeTotal = quantidadeTotal + item.quantidade;
        valorTotal = valorTotal + item.quantidade * item.preco;
    }

    if (quantidadeTotal === 0) {
        mensagem.textContent = "Adicione um cupcake antes de revisar o pedido.";
        return;
    }

    const nome = document.getElementById("cliente-nome").value.trim();
    const telefone = document.getElementById("cliente-telefone").value.trim();
    const endereco = document.getElementById("cliente-endereco").value.trim();

    if (nome === "" || telefone === "" || endereco === "") {
        mensagem.textContent = "Preencha nome, telefone e endereço.";
        return;
    }

    mensagem.textContent = 
    "Confira os dados: " + nome +
    " | Telefone: " + telefone +
    " | Endereço: " + endereco +
    " | Quantidade: " + quantidadeTotal +
    " | Total: " + formatarMoeda(valorTotal) +
    ". Esta é uma revisão. O pedido ainda não foi enviado.";
}

async function iniciarLoja() {
    const vitrine = document.getElementById("vitrine");
    const botaoFinalizar = document.getElementById("botao-finalizar");
    const botaoEsvaziar = document.getElementById("botao-esvaziar");

    vitrine.textContent = "Carregando produtos...";
    botaoFinalizar.disabled = true;
    botaoEsvaziar.disabled = true;

    try {
        const resposta = await fetch("/api/produtos");

        if (!resposta.ok) {
            throw new Error("Não foi possível buscar os produtos.");
        }

        produtos = await resposta.json();

        for (const item of produtos) {
            item.quantidade = 0;
        }

        carregarCarrinho();
        mostrarProdutos();
        atualizarCarrinho();
    
        botaoFinalizar.disabled = false;
    
    } catch (erro) {
        vitrine.textContent =
            "Não foi possível carregar os produtos. Atualize a página para tentar novamente.";

        console.error("Erro ao iniciar a loja:", erro);
    }
    
}

iniciarLoja();

document.getElementById("formulario-pedido")
    .addEventListener("submit", revisarPedido);

document.getElementById("formulario-pedido")
    .addEventListener("input", function () {
        document.getElementById("mensagem-pedido").textContent = "";
    });