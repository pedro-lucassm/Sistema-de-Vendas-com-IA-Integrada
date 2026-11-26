from database import conectar

def criar_cliente(nome_cliente, tipo_doc, cpf_cnpj, telefone, email, cep, rua, numero, cidade, estado):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        INSERT INTO clientes (nome_cliente, tipo_doc, cpf_cnpj, telefone, email, cep, rua, numero, cidade, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = nome_cliente, tipo_doc, cpf_cnpj, telefone, email, cep, rua, numero, cidade, estado

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM clientes WHERE status = 'Ativo' ORDER BY id_cliente")
    resultado = cursor.fetchall()

    cursor.close()
    conexao.close()

    return resultado

def excluir_cliente(id_cliente):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
        UPDATE clientes
        SET status = 'Desativado'
        WHERE id_cliente = %s
    """
    cursor.execute(sql, (id_cliente,))
    conexao.commit()

    cursor.close()
    conexao.close()