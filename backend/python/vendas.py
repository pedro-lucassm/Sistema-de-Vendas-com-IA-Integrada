#Importar a função (conexão com o banco) do outro arquivo
from database import conectar

#CREATE
def criar_venda(cliente, moto_modelo, moto_placa, servico_produto, valor):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO vendas (cliente, moto_modelo, moto_placa, servico_produto, valor)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (cliente, moto_modelo, moto_placa, servico_produto, valor))
    conexao.commit()

    cursor.close()
    conexao.close()


#READ
def listar_vendas():
    conexao = conectar()
    cursor = conexao.cursor() 

    cursor.execute('SELECT * FROM vendas ORDER BY id_venda DESC')
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultado


#UPDATE
def atualizar_venda(valor_novo, id_venda):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE vendas
        SET valor = %s 
        WHERE id_venda = %s   
    """
    cursor.execute(sql, (valor_novo, id_venda))
    conexao.commit()

    cursor.close()
    conexao.close()


#DELETE
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
