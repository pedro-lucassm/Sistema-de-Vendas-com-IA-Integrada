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

def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM produtos WHERE status = 'Ativo'")
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultado


def excluir_produto(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE produtos
        SET status = 'Desativado'
        WHERE id_produto = %s
    """
    cursor.execute(sql, (id_produto,))
    conexao.commit()

    cursor.close()
    conexao.close()