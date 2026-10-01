        let quantidade = 0;
        const produtos = [
            {
                nome: "Cupcake de Morango",
                descricao: "Massa de morango com cobertura de chantilly.",
                preco: 8.00
            },
            {
                nome: "Cupcake de chocolate",
                descricao: "Massa de chocolate com cobertura de brigadeiro.",
                preco: 10.00
            }
        ];

        const produto = produtos[0];

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
                preco.textContent = "Preço: " + item.preco.toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL"
                });
                cartao.append(nome, descricao, preco);
                vitrine.append(cartao);
            }
        }

        function atualizarCarrinho() {
            const total = quantidade * produto.preco;

            document.getElementById("carrinho").textContent =
                "Itens no carrinho: " + quantidade;

            document.getElementById("total").textContent = 
                "Total: " + total.toLocaleString("pt-BR", {
                    style: "currency",
                    currency: "BRL"
                });

                document.getElementById("botao-remover").disabled = quantidade === 0;
                document.getElementById("botao-esvaziar").disabled = quantidade === 0;
        }

        function adicionarAoCarrinho() {
            quantidade = quantidade + 1;
            atualizarCarrinho();
        }

        function removerDoCarrinho() {
            if (quantidade > 0) {
                quantidade = quantidade - 1;
                atualizarCarrinho();
            }
        }

        function esvaziarCarrinho() {
            quantidade = 0;
            atualizarCarrinho();
        }
        mostrarProdutos();
        atualizarCarrinho();