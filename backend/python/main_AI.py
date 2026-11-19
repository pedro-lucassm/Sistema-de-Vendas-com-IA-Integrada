import ollama
import json
import requests

def resposta_ia(pergunta_usuario: str) -> str:
    base_url = "http://127.0.0.1:8000"
    
    # Busca os dados atualizados
    vendas = requests.get(f"{base_url}/vendas").json()
    clientes = requests.get(f"{base_url}/clientes").json()
    produtos = requests.get(f"{base_url}/produtos").json()

    contexto_geral = {
        "vendas": vendas,
        "clientes": clientes,
        "produtos": produtos
    }
    
    dados_formatados = json.dumps(contexto_geral, ensure_ascii=False, indent=2)

    prompt = f""" 
    Você é o assistente virtual de inteligência de negócios da Oficina Mecânica.
    Sua função é responder a dúvidas sobre vendas, faturamento, clientes, serviços e produtos com base EXCLUSIVAMENTE nos dados abaixo.

    REGRAS DE RESPOSTA:
    1. Responda de forma direta, cortês e profissional.
    2. Se a informação solicitada estiver nos dados, responda com precisão e inclua valores formatados em R$.
    3. Se o usuário perguntar algo que NÃO está nos dados fornecidos, diga educadamente que não possui essa informação no momento.
    4. Não invente ou calcule valores que contradigam os dados.

    --- DADOS DA OFICINA ---
    {dados_formatados}
    ------------------------

    Pergunta do usuário: {pergunta_usuario}
    """
    
    response = ollama.chat(
        model='gemma4:e4b',
        messages=[{'role': 'user', 'content': prompt}],
        options={'temperature': 0.2}
    )
    
    return response['message']['content']