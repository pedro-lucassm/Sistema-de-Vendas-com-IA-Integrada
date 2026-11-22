import requests

BASE_URL = "http://127.0.0.1:8000"

def calcular_faturamento():
    """
    Calcula o faturamento total da oficina
    com base nas vendas cadastradas.
    """

    vendas = requests.get(f"{BASE_URL}/vendas").json()

    total = sum(
        float(venda["valor_total"])
        for venda in vendas
    )

    return {
        "faturamento": round(total, 2)
    }

def calcular_ticket_medio():
    """
    Calcula o ticket médio das vendas da oficina.

    Returns:
        dict: Quantidade de vendas e ticket médio.
    """

    resposta = requests.get(f"{BASE_URL}/vendas")

    vendas = resposta.json()

    faturamento = sum(
        float(venda["valor_total"])
        for venda in vendas
    )

    ticket_medio = faturamento / len(vendas)

    return {
        "quantidade_vendas": len(vendas),
        "faturamento": round(faturamento, 2),
        "ticket_medio": round(ticket_medio, 2)
    }

def contar_vendas():
    """
    Retorna a quantidade de vendas feitas na oficina.

    Returns:
        dict: Quantidade de vendas.
    """
    resposta = requests.get(f"{BASE_URL}/vendas")

    vendas = resposta.json()

    return{
        "quantidade_vendas": len(vendas)
    }

def contar_clientes():
    """
    Retorna a quantidade de clientes cadastrados
    na oficina.

    Returns:
        dict: Quantidade de clientes.
    """

    resposta = requests.get(f"{BASE_URL}/clientes")

    clientes = resposta.json()

    return{
        "quantidade_clientes": len(clientes)
    }
