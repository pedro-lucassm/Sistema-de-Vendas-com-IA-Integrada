async function carregarVendas() {
    try {

        const resposta = await fetch('http://127.0.0.1:8000/vendas');
        const vendas = await resposta.json();

        const principal = document.getElementById('table');

        // Cabeçalho da tabela
        let tabela = `
                <thead class="table-light">
                    <tr>
                        <th scope="col">ID</th>
                        <th scope="col">CLIENTE</th>
                        <th scope="col">MODELO MOTO</th>
                        <th scope="col">PLACA</th>
                        <th scope="col">SERVIÇO/PRODUTO</th>
                        <th scope="col">VALOR</th>
                        <th scope="col" class="w-25">EDITAR / EXCLUIR</th>
                    </tr>
                </thead>
                <tbody class="table-group-divider">
        `

        //Dados da tabela
        vendas.forEach(venda => {
                tabela += `
                            <tr>
                                <th>${venda['id_venda']}</th>
                                <td>${venda['cliente']}</td>
                                <td>${venda['moto_modelo']}</td>
                                <td>${venda['moto_placa']}</td>
                                <td>${venda['servico_produto']}</td>
                                <td>R$ ${venda['valor'].toFixed(2)}</td>
                                <td class="d-flex justify-content-center gap-3"><button type="button" class="btn btn-warning w-25 py-2 mb-2" onclick="window.location.href=''">&#9999</button> <button type="button" class="btn btn-danger w-25 py-2 mb-2" onclick="window.location.href=''">&#128465</button></td>
                            </tr>

                `;
        });

        tabela += `</tbody>`
        principal.innerHTML = tabela;

    } catch(erro){
        console.error('Erro ao buscar as vendas', erro)
    }
}

carregarVendas();