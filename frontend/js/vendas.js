const principal = document.getElementById('table');

let tabela = `
        <thead class="table-light">
            <tr>
                <th scope="col">ID</th>
                <th scope="col">Produto</th>
                <th scope="col">Valor</th>
                <th scope="col" class="w-25">Ação</th>
            </tr>
        </thead>
        <tbody class="table-group-divider">
`

for (let i = 1; i <= 20; i++) {
    tabela += `
                <tr>
                    <th>${[i]}</th>
                    <td>Mark</td>
                    <td>$ ${[i] * 10}</td>
                    <td class="d-flex justify-content-center gap-3"><button type="button" class="btn btn-warning w-25 py-2 mb-2" onclick="window.location.href=''">&#9999</button> <button type="button" class="btn btn-danger w-25 py-2 mb-2" onclick="window.location.href=''">&#128465</button></td>
                </tr>

    `;
}

tabela += `</tbody>`

principal.innerHTML = tabela;