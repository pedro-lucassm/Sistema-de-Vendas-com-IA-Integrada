const formProduto = document.getElementById('form-produto');

formProduto.addEventListener('submit', async (event) => {
    event.preventDefault();

    const produtoData = {
        nome_produto: document.getElementById('nome').value,
        categoria: document.getElementById('categoria').value,
        preco_custo: document.getElementById('preco_custo').value,
        preco_venda: document.getElementById('preco_venda').value,
        estoque: document.getElementById('estoque').value
    };

    const response = await fetch('http://localhost:8000/cadastro_produtos',{
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(produtoData)
    });

    const resultado = await response.json();

    if (response.ok) {
        alert('Produto cadastrado com sucesso!');
        formProduto.reset();
    } else {
        alert('Erro ao cadastrar: ' + JSON.stringify(resultado.detail));
    }
});