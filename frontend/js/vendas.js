async function carregarVendas() {
    try {

        const resposta = await fetch('http://127.0.0.1:8000/vendas');
        const vendas = await resposta.json();

        const principal = document.getElementById('table');

        // Cabeçalho da tabela
        let tabela = `
                <thead class="table-light">
                    <tr>
                        <th scope="col">ID VENDA</th>
                        <th scope="col">CLIENTE</th>
                        <th scope="col">TOTAL</th>
                        <th scope="col" class="w-25">EXCLUIR</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider">
        `
        //Dados da tabela
        vendas.forEach(venda => {
                tabela += `
                            <tr>
                                <td>${venda['id_venda']}</td>
                                <td>${venda['nome_cliente']}</td>
                                <td>R$ ${venda['valor_total']}</td>
                                <td class="d-flex justify-content-center gap-3"><button type="button" class="btn btn-danger w-25 py-2 mb-2" onclick="window.location.href=''">&#128465</button></td>
                            </tr>

                `;
        });

        tabela += `</tbody>`
        principal.innerHTML = tabela;

    } catch(erro){
        console.error('Erro ao buscar as vendas', erro)
    }
};

carregarVendas();