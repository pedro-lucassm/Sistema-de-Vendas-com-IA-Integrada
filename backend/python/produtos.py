from database import conectar

def criar_produto(nome_produto, categoria, preco_custo, preco_venda, estoque):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO produtos (nome_produto, categoria, preco_custo, preco_venda, estoque)
        VALUES (%s, %s, %s, %s, %s)
    """

    valores = nome_produto, categoria, preco_custo, preco_venda, estoque

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()