        let quantidade = 0;
        const preco = 8.00;

        function atualizarCarrinho() {
            const total = quantidade * preco;

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
        atualizarCarrinho();