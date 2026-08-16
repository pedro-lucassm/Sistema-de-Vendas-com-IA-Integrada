# Funções do Sistema
from database import conectar

#Importar a função (conexão com o banco) do outro arquivo
from database import conectar

#CREATE
def criar_venda(nome_produto, valor):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO vendas (nome_produto, valor)
        VALUES (%s, %s)
    """
    cursor.execute(sql, (nome_produto, valor))
    conexao.commit()

    cursor.close()
    conexao.close()


#READ
def listar_vendas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM vendas')
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
        WHERE idVenda = %s   
    """
    cursor.execute(sql,(valor_novo, id_venda))
    conexao.commit()

    cursor.close()
    conexao.close()


#DELETE
def excluir_venda(id_venda):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        DELETE
        FROM vendas
        WHERE idVenda = %s
    """
    cursor.execute(sql, (id_venda,))
    conexao.commit()

    cursor.close()
    conexao.close
