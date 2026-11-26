let todasVendas = []; // Guarda as vendas carregadas da API na memória

// 1. Busca os dados da API uma única vez
async function carregarVendas() {
    try {
        const resposta = await fetch('http://127.0.0.1:8000/vendas');
        todasVendas = await resposta.json();
        renderizarTabela(todasVendas); // Exibe todas as vendas inicialmente
    } catch (erro) {
        console.error('Erro ao buscar as vendas', erro);
    }
}

// 2. Desenha a tabela na tela com a lista recebida
function renderizarTabela(listaVendas) {
    const principal = document.getElementById('table');

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
    `;

    if (listaVendas.length === 0) {
        tabela += `
            <tr>
                <td colspan="4" class="text-center py-3 text-secondary">Nenhuma venda encontrada para este cliente.</td>
            </tr>
        `;
    } else {
        listaVendas.forEach(venda => {
            tabela += `
                <tr>
                    <td>${venda['id_venda']}</td>
                    <td>${venda['nome_cliente']}</td>
                    <td>R$ ${venda['valor_total']}</td>
                    <td class="d-flex justify-content-center gap-3">
                        <button type="button" class="btn btn-danger w-25 py-2 mb-2" onclick="excluirVenda(${venda['id_venda']})">&#128465;</button>
                    </td>
                </tr>
            `;
        });
    }

    tabela += `</tbody>`;
    principal.innerHTML = tabela;
}

// 3. Filtra pelo nome do cliente
function filtrarVendas() {
    const termo = document.getElementById('input-pesquisa').value.toLowerCase().trim();
    
    const vendasFiltradas = todasVendas.filter(venda => 
        venda['nome_cliente'].toLowerCase().includes(termo)
    );

    renderizarTabela(vendasFiltradas);
}

// Eventos: filtra ao digitar e ao clicar no botão
document.getElementById('input-pesquisa').addEventListener('input', filtrarVendas);
document.getElementById('btn-pesquisar').addEventListener('click', filtrarVendas);

async function excluirVenda(idVenda) {
    const confirmou = confirm(`Tem certeza que deseja excluir a venda #${idVenda}? Essa ação não pode ser desfeita.`);
    
    if (!confirmou) return; 

    try {
        const resposta = await fetch(`http://127.0.0.1:8000/vendas/${idVenda}`, {
            method: 'DELETE'
        });

        if (resposta.ok) {

            todasVendas = todasVendas.filter(venda => venda['id_venda'] !== idVenda);
            filtrarVendas();
            alert('Não foi possível excluir a venda. Verifique no servidor.');
        }
    } catch (erro) {
        console.error('Erro ao excluir a venda:', erro);
        alert('Erro de conexão ao tentar excluir a venda.');
    }
}

// Inicia carregando os dados
carregarVendas();