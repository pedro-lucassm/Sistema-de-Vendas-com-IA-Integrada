from google import genai
import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

# Inicializa o cliente oficial
client = genai.Client(api_key=os.getenv('API_KEY'))

# Função para fazer requisições para IA
def perguntar_ao_assistente(pergunta_usuario, contexto_dados):
    dados_formatados = json.dumps(contexto_dados, ensure_ascii=False, indent=2)

    prompt = f""" 
    Você é o assistente virtual de inteligência de negócios da Oficina Mecânica.
    Sua função é responder a dúvidas sobre vendas, faturamento, serviços prestados, clientes e produtos com base EXCLUSIVAMENTE no dicionário de dados abaixo.

    REGRAS DE RESPOSTA:
    1. Responda de forma direta, cortês e profissional.
    2. Se a informação solicitada estiver no dicionário, responda com precisão e inclua os valores formatados em R$.
    3. Se o usuário perguntar algo que NÃO está nos dados fornecidos, diga educadamente que não possui essa informação no momento.
    4. Não invente ou calcule valores que contradigam o dicionário.

    --- DADOS DE VENDAS DA OFICINA ---
    {dados_formatados}
    ---------------------------------

    Pergunta do usuário: {pergunta_usuario}
    """
    
    # Chamada do modelo no novo SDK
    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt,
    )
    return response.text

if __name__ == "__main__":
    try:
        # Faz a requisição na rota do seu FastAPI que está rodando localmente
        resposta_api = requests.get("http://127.0.0.1:8000/vendas")
        
        if resposta_api.status_code == 200:
            # Converte o retorno da API em objeto Python (lista de dicionários)
            dados_vendas = resposta_api.json()
            
            # Pergunta para o assistente usando os dados reais da sua API
            pergunta = "Quem foi o cliente com mais vendas?"
            
            resposta_ia = perguntar_ao_assistente(pergunta, dados_vendas)
            print("Resposta da IA:\n", resposta_ia)
        else:
            print("Erro ao acessar a API do FastAPI. Status:", resposta_api.status_code)
            
    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível conectar ao FastAPI. Verifique se o servidor está rodando na porta 8000!")