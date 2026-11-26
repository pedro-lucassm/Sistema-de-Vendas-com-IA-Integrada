let todosProdutos = []; // Guarda os produtos carregados da API na memória


// 1. Busca os produtos da API uma única vez
async function carregarProdutos() {

    try {

        const resposta = await fetch('http://127.0.0.1:8000/produtos');

        todosProdutos = await resposta.json();

        renderizarTabela(todosProdutos);

    } catch (erro) {

        console.error('Erro ao buscar os produtos:', erro);

    }
}


// 2. Desenha a tabela na tela
function renderizarTabela(listaProdutos) {

    const principal = document.getElementById('table');

    let tabela = `
        <thead class="table-light">

            <tr>

                <th scope="col">
                    ID PRODUTO
                </th>

                <th scope="col">
                    PRODUTO
                </th>

                <th scope="col">
                    PREÇO
                </th>

                <th scope="col">
                    ESTOQUE
                </th>

                <th scope="col" class="w-25">
                    EXCLUIR
                </th>

            </tr>

        </thead>

        <tbody class="table-group-divider">
    `;


    // Caso não existam produtos
    if (listaProdutos.length === 0) {

        tabela += `
            <tr>

                <td colspan="5"
                    class="text-center py-3 text-secondary">

                    Nenhum produto encontrado.

                </td>

            </tr>
        `;

    } else {

        listaProdutos.forEach(produto => {

            tabela += `
                <tr>

                    <td>
                        ${produto['id_produto']}
                    </td>

                    <td>
                        ${produto['nome_produto']}
                    </td>

                    <td>
                        R$ ${Number(produto['preco_venda'])}
                    </td>

                    <td>
                        ${produto['estoque']}
                    </td>

                    <td class="d-flex justify-content-center gap-3">

                        <button
                            type="button"
                            class="btn btn-danger w-25 py-2 mb-2"
                            onclick="excluirProduto(${produto['id_produto']})">

                            &#128465;

                        </button>

                    </td>

                </tr>
            `;

        });

    }

    tabela += `</tbody>`;

    principal.innerHTML = tabela;
}


// 3. Filtra os produtos pelo nome
function filtrarProdutos() {

    const termo =
        document
            .getElementById('input-pesquisa')
            .value
            .toLowerCase()
            .trim();


    const produtosFiltrados = todosProdutos.filter(produto => {

        return String(produto['nome_produto'])
            .toLowerCase()
            .includes(termo);

    });


    renderizarTabela(produtosFiltrados);
}


// 4. Eventos da pesquisa

document
    .getElementById('input-pesquisa')
    .addEventListener('input', filtrarProdutos);


document
    .getElementById('btn-pesquisar')
    .addEventListener('click', filtrarProdutos);


// 5. Excluir produto
async function excluirProduto(idProduto) {

    const confirmou = confirm(
        `Tem certeza que deseja excluir o produto #${idProduto}? Essa ação não pode ser desfeita.`
    );


    if (!confirmou) return;


    try {

        const resposta = await fetch(
            `http://127.0.0.1:8000/produtos/${idProduto}`,
            {
                method: 'DELETE'
            }
        );


        if (resposta.ok) {

            todosProdutos = todosProdutos.filter(
                produto => produto['id_produto'] !== idProduto
            );

            filtrarProdutos();

            alert('Produto excluído com sucesso!');

        } else {

            alert('Não foi possível excluir o produto. Verifique no servidor.');

        }

    } catch (erro) {

        console.error(
            'Erro ao excluir o produto:',
            erro
        );

        alert(
            'Erro de conexão ao tentar excluir o produto.'
        );

    }

}

// Inicia carregando os produtos
carregarProdutos();