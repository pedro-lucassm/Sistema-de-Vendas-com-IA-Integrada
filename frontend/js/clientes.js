let todosClientes = []; // Guarda os clientes carregados da API na memória


// 1. Busca os dados da API uma única vez
async function carregarClientes() {

    try {

        const resposta = await fetch(
            'http://127.0.0.1:8000/clientes'
        );

        todosClientes = await resposta.json();

        renderizarTabela(todosClientes);

    } catch (erro) {

        console.error('Erro ao buscar os clientes:', erro);

    }

}


// 2. Desenha a tabela na tela com a lista recebida
function renderizarTabela(listaClientes) {

    const principal = document.getElementById('table');

    let tabela = `
        <thead class="table-light">

            <tr>

                <th scope="col">
                    ID CLIENTE
                </th>

                <th scope="col">
                    NOME
                </th>

                <th scope="col">
                    EMAIL
                </th>

                <th scope="col">
                    TELEFONE
                </th>

                <th scope="col" class="w-25">
                    EXCLUIR
                </th>

            </tr>

        </thead>

        <tbody class="table-group-divider">
    `;


    // Caso não existam clientes
    if (listaClientes.length === 0) {

        tabela += `
            <tr>

                <td
                    colspan="5"
                    class="text-center py-3 text-secondary">
                    Nenhum cliente encontrado.
                </td>

            </tr>
        `;

    } else {

        listaClientes.forEach(cliente => {

            tabela += `

                <tr>

                    <td>
                        ${cliente['id_cliente']}
                    </td>

                    <td>
                        ${cliente['nome_cliente']}
                    </td>

                    <td>
                        ${cliente['email']}
                    </td>

                    <td>
                        ${cliente['telefone']}
                    </td>

                    <td class="d-flex justify-content-center gap-3">

                        <button
                            type="button"
                            class="btn btn-danger w-25 py-2 mb-2"
                            onclick="excluirCliente(${cliente['id_cliente']})">

                            &#128465;

                        </button>

                    </td>

                </tr>

            `;

        });

    }


    tabela += `
        </tbody>
    `;

    principal.innerHTML = tabela;

}


// 3. Filtra pelo nome do cliente
function filtrarClientes() {

    const termo = document
        .getElementById('input-pesquisa')
        .value
        .toLowerCase()
        .trim();


    const clientesFiltrados = todosClientes.filter(cliente => {

        const nome = String(cliente['nome_cliente'] || '')
            .toLowerCase();

        const email = String(cliente['email'] || '')
            .toLowerCase();

        const telefone = String(cliente['telefone'] || '')
            .toLowerCase();


        return (
            nome.includes(termo) ||
            email.includes(termo) ||
            telefone.includes(termo)
        );

    });


    renderizarTabela(clientesFiltrados);

}


// Eventos:
// filtra ao digitar
document
    .getElementById('input-pesquisa')
    .addEventListener('input', filtrarClientes);


// filtra ao clicar no botão
document
    .getElementById('btn-pesquisar')
    .addEventListener('click', filtrarClientes);


// 4. Excluir cliente
async function excluirCliente(idCliente) {

    const confirmou = confirm(
        `Tem certeza que deseja excluir o cliente #${idCliente}? Essa ação não pode ser desfeita.`
    );


    if (!confirmou) return;


    try {

        const resposta = await fetch(
            `http://127.0.0.1:8000/clientes/${idCliente}`,
            {
                method: 'DELETE'
            }
        );


        if (resposta.ok) {

            todosClientes = todosClientes.filter(
                cliente => cliente['id_cliente'] !== idCliente
            );

            filtrarClientes();

            alert('Cliente excluído com sucesso.');

        } else {

            alert(
                'Não foi possível excluir o cliente. Verifique no servidor.'
            );

        }


    } catch (erro) {

        console.error(
            'Erro ao excluir o cliente:',
            erro
        );

        alert(
            'Erro de conexão ao tentar excluir o cliente.'
        );

    }

}


// Inicia carregando os dados
carregarClientes();