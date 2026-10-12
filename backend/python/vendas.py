from database import conectar

# CREATE
def criar_venda(dados):
    conexao = conectar()
    cursor = conexao.cursor()

    sql_venda = """
        INSERT INTO vendas (id_cliente, data_venda, valor_total)
        VALUES (%s, %s, %s)
        RETURNING id_venda;
    """
    cursor.execute(sql_venda, (dados.id_cliente, dados.data_venda, dados.valor_total))
    
    row = cursor.fetchone()
    if not row:
        raise Exception("Erro ao inserir a venda: ID não retornado.")
    
    if isinstance(row, dict):
        id_venda = row.get("id_venda")
    else:
        id_venda = row[0]

    for item in dados.itens:
        sql_item = """
            INSERT INTO itens_venda (id_venda, id_produto, quantidade, preco_unitario, subtotal)
            VALUES (%s, %s, %s, %s, %s);
        """
        cursor.execute(
            sql_item, 
            (id_venda, item.id_produto, item.quantidade, item.preco_unitario, item.subtotal)
        )

    conexao.commit()

    cursor.close()
    conexao.close()


# READ
def listar_vendas():
    conexao = conectar()
    cursor = conexao.cursor() 

    sql = """
            SELECT 
                vd.id_venda,
                c.nome_cliente,
                vd.data_venda,
                vd.valor_total
            FROM vendas vd
            JOIN clientes c on (vd.id_cliente = c.id_cliente)
            ORDER BY id_venda DESC
        """

    cursor.execute(sql) 
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultado


# UPDATE
def atualizar_venda(valor_novo, id_venda):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE vendas
        SET valor_total = %s 
        WHERE id_venda = %s   
    """ 
    cursor.execute(sql, (valor_novo, id_venda))
    conexao.commit()

    cursor.close()
    conexao.close()


# DELETE
def excluir_venda(id_venda):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        DELETE FROM vendas
        WHERE id_venda = %s
    """
    cursor.execute(sql, (id_venda,))
    conexao.commit()

    cursor.close()
    conexao.close()