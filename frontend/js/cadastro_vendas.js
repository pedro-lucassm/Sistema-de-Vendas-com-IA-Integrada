// Variável global para guardar os produtos carregados da API
let listaProdutosGlobais = [];

// Clientes
const selectCliente = document.getElementById('select_cliente');
async function carregarClientes() {
    try {
        const response = await fetch('http://localhost:8000/clientes');
        if (!response.ok) throw new Error('Erro ao buscar clientes');

        const clientes = await response.json();
        selectCliente.innerHTML = '<option value="" selected disabled>Selecione um cliente...</option>';

        clientes.forEach(cliente => {
            const option = document.createElement('option');
            option.value = cliente.id_cliente; 
            option.textContent = cliente.nome_cliente;
            selectCliente.appendChild(option);
        });
    } catch (erro) {
        console.error('Erro ao carregar lista de clientes:', erro);
    }
}

// Produtos
const selectProduto = document.getElementById('select_produto');
const inputPrecoUnitario = document.getElementById('preco_unitario');

async function carregarProdutos() {
    try {
        const response = await fetch('http://localhost:8000/produtos');
        if (!response.ok) throw new Error('Erro ao buscar produtos');

        listaProdutosGlobais = await response.json();

        selectProduto.innerHTML = '<option value="" selected disabled>Selecione produto...</option>';

        listaProdutosGlobais.forEach(produto => {
            const option = document.createElement('option');
            option.value = produto.id_produto; 
            option.textContent = produto.nome_produto;
            selectProduto.appendChild(option);
        });
    } catch (erro) {
        console.error('Erro ao carregar lista de produtos:', erro);
    }
}

selectProduto.addEventListener('change', (event) => {
    const idProdutoSelecionado = parseInt(event.target.value);

    const produtoEncontrado = listaProdutosGlobais.find(p => p.id_produto === idProdutoSelecionado);

    if (produtoEncontrado) {
        inputPrecoUnitario.value = produtoEncontrado.preco_venda || produtoEncontrado.preco || 0.00;
    } else {
        inputPrecoUnitario.value = '';
    }
});

// Array para armazenar os itens adicionados na venda atual
let itensDaVenda = [];

const btnAdicionarItem = document.getElementById('btn-adicionar-item');
const inputQuantidade = document.getElementById('quantidade');
const corpoTabelaItens = document.getElementById('corpo-tabela-itens');
const spanValorTotal = document.getElementById('valor_total_exibicao');

btnAdicionarItem.addEventListener('click', () => {
    const idProdutoSelecionado = parseInt(selectProduto.value);
    const quantidade = parseInt(inputQuantidade.value);
    const precoUnitario = parseFloat(inputPrecoUnitario.value);

    // Validações básicas
    if (!idProdutoSelecionado || isNaN(idProdutoSelecionado)) {
        alert('Por favor, selecione um produto.');
        return;
    }

    if (!quantidade || quantidade <= 0) {
        alert('A quantidade deve ser maior que zero.');
        return;
    }

    // Busca o nome do produto na lista global para exibir na tabela
    const produtoObj = listaProdutosGlobais.find(p => p.id_produto === idProdutoSelecionado);
    const nomeProduto = produtoObj ? produtoObj.nome_produto : 'Produto';

    // Calcula o subtotal do item
    const subtotal = quantidade * precoUnitario;

    // Adiciona o item no array local da venda
    const novoItem = {
        id_produto: idProdutoSelecionado,
        nome: nomeProduto,
        quantidade: quantidade,
        preco_unitario: precoUnitario,
        subtotal: subtotal
    };

    itensDaVenda.push(novoItem);

    // Atualiza a tabela e o valor total na tela
    atualizarTabelaItens();

    // Reseta os campos de produto e quantidade para o próximo item
    selectProduto.value = "";
    inputPrecoUnitario.value = "";
    inputQuantidade.value = "1";
});

// Função para renderizar os itens na tabela HTML
function atualizarTabelaItens() {
    corpoTabelaItens.innerHTML = '';
    let valorTotalGeral = 0;

    itensDaVenda.forEach((item, index) => {
        valorTotalGeral += item.subtotal;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${item.nome}</td>
            <td class="text-center">${item.quantidade}</td>
            <td class="text-end">R$ ${item.preco_unitario.toFixed(2)}</td>
            <td class="text-end">R$ ${item.subtotal.toFixed(2)}</td>
            <td class="text-center">
                <button type="button" class="btn btn-danger btn-sm" onclick="removerItem(${index})">Remover</button>
            </td>
        `;
        corpoTabelaItens.appendChild(tr);
    });

    // Atualiza o span do total geral da venda
    spanValorTotal.textContent = valorTotalGeral.toFixed(2);
}

// Função para remover um item da lista
window.removerItem = function(index) {
    itensDaVenda.splice(index, 1);
    atualizarTabelaItens();
};

const formVenda = document.getElementById('form-venda');
const inputDataVenda = document.getElementById('data_venda');

formVenda.addEventListener('submit', async (event) => {
    event.preventDefault(); // Impede o recarregamento padrão da página

    const idCliente = parseInt(selectCliente.value);
    const dataVenda = inputDataVenda.value;
    const valorTotal = parseFloat(spanValorTotal.textContent);

    // Validações antes de enviar
    if (!idCliente || isNaN(idCliente)) {
        alert('Por favor, selecione um cliente.');
        return;
    }

    if (!dataVenda) {
        alert('Por favor, informe a data e hora da venda.');
        return;
    }

    if (itensDaVenda.length === 0) {
        alert('Adicione pelo menos um produto na tabela antes de finalizar a venda.');
        return;
    }

    // Monta o objeto no formato exato que o VendaCreateSchema do FastAPI espera
    const vendaPayload = {
        id_cliente: idCliente,
        data_venda: dataVenda, // O formato 'datetime-local' (YYYY-MM-DDTHH:mm) é aceito pelo Pydantic
        valor_total: valorTotal,
        itens: itensDaVenda.map(item => ({
            id_produto: item.id_produto,
            quantidade: item.quantidade,
            preco_unitario: item.preco_unitario,
            subtotal: item.subtotal
        }))
    };

    try {
        const response = await fetch('http://localhost:8000/cadastro_vendas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(vendaPayload)
        });

        const resultado = await response.json();

        if (response.ok) {
            alert('Venda cadastrada com sucesso!');
            formVenda.reset();          // Limpa o formulário
            itensDaVenda = [];          // Esvazia a lista local de itens
            atualizarTabelaItens();     // Limpa a tabela na tela
            spanValorTotal.textContent = '0.00';
        } else {
            alert('Erro ao cadastrar venda: ' + JSON.stringify(resultado.detail || resultado));
        }

    } catch (erro) {
        console.error('Erro de conexão:', erro);
        alert('Erro ao conectar com o servidor. Verifique se o FastAPI está rodando.');
    }
});

carregarClientes();
carregarProdutos();