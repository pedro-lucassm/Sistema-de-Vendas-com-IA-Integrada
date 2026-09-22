const formCliente = document.getElementById('form-cliente');


formCliente.addEventListener('submit', async (event) => {
    event.preventDefault();
    
    const clienteData = {
        nome_cliente: document.getElementById('nome').value,
        tipo_doc: document.getElementById('tipo_doc').value,
        cpf_cnpj: document.getElementById('cpf_cnpj').value,
        telefone: document.getElementById('telefone').value,
        email: document.getElementById('email').value || null,
        cep: document.getElementById('cep').value || null,
        rua: document.getElementById('rua').value || null,
        numero: document.getElementById('numero').value || null,
        cidade: document.getElementById('cidade').value || null,
        estado: document.getElementById('estado').value || null
    };

    const response = await fetch('http://localhost:8000/cadastro_clientes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(clienteData)
    });

    const resultado = await response.json();

    // Retorno visual para você saber se funcionou
    if (response.ok) {
        alert('Cliente cadastrado com sucesso!');
        formCliente.reset();
    } else {
        alert('Erro ao cadastrar: ' + JSON.stringify(resultado.detail));
    }
});