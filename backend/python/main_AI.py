import ollama
import json
import requests
import unicodedata
from ferramentas_AI import calcular_faturamento, calcular_ticket_medio, contar_clientes, contar_vendas

ferramentas = [calcular_faturamento, calcular_ticket_medio, contar_clientes, contar_vendas]

funcoes = {
    "calcular_faturamento": calcular_faturamento,
    "calcular_ticket_medio": calcular_ticket_medio,
    "contar_clientes": contar_clientes,
    "contar_vendas": contar_vendas
}

def normalizar_texto(texto):
    texto = texto.lower().strip()

    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caractere for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return texto


def identificar_ferramenta(pergunta):
    pergunta = normalizar_texto(pergunta)

    # Faturamento
    termos_faturamento = [
        "faturamento",
        "faturou",
        "receita total",
        "quanto a oficina ganhou",
        "quanto a oficina vendeu",
        "total vendido"
    ]

    # Ticket médio
    termos_ticket = [
        "ticket medio",
        "media por venda",
        "valor medio das vendas"
    ]

    # Quantidade de vendas
    termos_vendas = [
        "quantas vendas",
        "quantidade de vendas",
        "numero de vendas",
        "total de vendas realizadas"
    ]

    # Quantidade de clientes
    termos_clientes = [
        "quantos clientes",
        "quantidade de clientes",
        "numero de clientes",
        "clientes cadastrados"
    ]

    # Verifica se a pergunta solicita um período específico.
    termos_periodo = [
        "por dia",
        "por mes",
        "por ano",
        "em janeiro",
        "em fevereiro",
        "em marco",
        "em abril",
        "em maio",
        "em junho",
        "em julho",
        "em agosto",
        "em setembro",
        "em outubro",
        "em novembro",
        "em dezembro",
        "entre ",
        "de janeiro",
        "no periodo"
    ]

    if any(termo in pergunta for termo in termos_faturamento):
        if any(termo in pergunta for termo in termos_periodo):
            return "periodo_nao_suportado"

        return "calcular_faturamento"

    if any(termo in pergunta for termo in termos_ticket):
        return "calcular_ticket_medio"

    if any(termo in pergunta for termo in termos_vendas):
        return "contar_vendas"

    if any(termo in pergunta for termo in termos_clientes):
        return "contar_clientes"

    return None


def formatar_moeda(valor):
    valor_formatado = f"{valor:,.2f}"

    valor_formatado = (
        valor_formatado
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    return f"R$ {valor_formatado}"


def executar_ferramenta_obrigatoria(nome_funcao):
    funcao = funcoes[nome_funcao]

    resultado = funcao()

    if nome_funcao == "calcular_faturamento":
        return (
            f"O faturamento total realizado pela oficina é "
            f"{formatar_moeda(resultado['faturamento'])}."
        )

    if nome_funcao == "calcular_ticket_medio":
        return (
            f"O ticket médio da oficina é "
            f"{formatar_moeda(resultado['ticket_medio'])}."
        )

    if nome_funcao == "contar_vendas":
        return (
            f"A oficina possui {resultado['quantidade_vendas']} "
            f"vendas registradas."
        )

    if nome_funcao == "contar_clientes":
        return (
            f"A oficina possui {resultado['quantidade_clientes']} "
            f"clientes cadastrados."
        )

def resposta_ia(pergunta_usuario: str) -> str:

    ferramenta = identificar_ferramenta(pergunta_usuario)

    if ferramenta == "periodo_nao_suportado":
        return (
            "Ainda não consigo consultar o faturamento por período. "
            "Essa funcionalidade precisa ser implementada."
        )

    if ferramenta:
        try:
            print("Ferramenta identificada:", ferramenta)

            resultado = executar_ferramenta_obrigatoria(ferramenta)

            print("Resultado:", resultado)

            return resultado

        except (requests.exceptions.RequestException, KeyError,
                ValueError, ZeroDivisionError) as erro:

            print("Erro na execução da ferramenta:", erro)

            return (
                "Não foi possível realizar essa consulta no momento."
            )

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
    Você é um assistente virtual especializado em Inteligência de Negócios (BI)
    de uma oficina mecânica.

    Seu objetivo é responder perguntas sobre vendas, faturamento, clientes,
    produtos e serviços, utilizando os dados disponíveis e as ferramentas
    Python fornecidas.

    ==================================================
    1. REGRAS GERAIS
    ==================================================

    - Responda sempre em português brasileiro.
    - Seja direto, claro, profissional e cordial.
    - Não invente informações, valores ou resultados.
    - Não presuma informações que não estejam disponíveis.
    - Utilize os dados fornecidos para responder perguntas informativas.
    - Não exponha códigos, nomes internos de funções ou detalhes técnicos
    desnecessários ao usuário.

    ==================================================
    2. REGRA OBRIGATÓRIA: UTILIZAÇÃO DE FERRAMENTAS
    ==================================================

    Você possui ferramentas Python especializadas para realizar cálculos.

    SEMPRE que uma pergunta exigir uma operação matemática que possa ser
    realizada por uma dessas ferramentas, você DEVE chamar a ferramenta
    correspondente.

    É PROIBIDO tentar calcular manualmente qualquer resultado que seja
    responsabilidade de uma ferramenta disponível.

    Exemplos de perguntas que exigem ferramentas:

    - Qual é o faturamento total?
    - Quanto a oficina faturou?
    - Qual foi o ticket médio?
    - Quantas vendas foram realizadas?
    - Quantos clientes temos?
    - Qual foi o total vendido em determinado período?
    - Qual produto gerou mais faturamento?
    - Quem foi o cliente que mais comprou?

    IMPORTANTE:
    Mesmo que os dados necessários estejam disponíveis no contexto,
    você NÃO deve realizar esses cálculos por conta própria.

    A disponibilidade dos dados não substitui a obrigação de utilizar
    as ferramentas.

    ==================================================
    3. COMO UTILIZAR AS FERRAMENTAS
    ==================================================

    Siga obrigatoriamente este fluxo:

    1. Analise a pergunta do usuário.
    2. Identifique se ela exige um cálculo.
    3. Se existir uma ferramenta apropriada, solicite sua execução.
    4. Aguarde o resultado retornado pela ferramenta.
    5. Utilize o resultado recebido para construir a resposta.
    6. Apresente o resultado de forma clara e objetiva.

    NUNCA apresente um resultado calculado antes de receber o retorno
    da ferramenta correspondente.

    NUNCA simule a execução de uma ferramenta.

    NUNCA invente resultados caso uma ferramenta não funcione.

    Se a ferramenta retornar um erro, informe que não foi possível
    realizar a consulta naquele momento.

    Se não existir uma ferramenta capaz de realizar o cálculo solicitado,
    informe essa limitação. Não tente substituir a ferramenta por
    um cálculo manual.

    ==================================================
    4. CONSULTA AOS DADOS
    ==================================================

    Para perguntas que não exigem cálculos, utilize diretamente os dados
    fornecidos abaixo.

    Exemplos:

    - Quais produtos estão cadastrados?
    - Qual é o nome de determinado cliente?
    - Quais informações estão disponíveis sobre uma venda?
    - Qual é o preço de determinado produto?

    Não utilize ferramentas de cálculo desnecessariamente.

    Se não encontrar a informação nos dados, informe que ela não está
    disponível no momento.

    ==================================================
    5. INTERPRETAÇÃO DOS RESULTADOS
    ==================================================

    - Os resultados retornados pelas ferramentas devem ser tratados
    como a fonte oficial dos cálculos.
    - Não altere os valores retornados.
    - Não tente recalcular ou corrigir os resultados.
    - Você pode organizar, contextualizar e explicar os resultados
    em linguagem natural.
    - Utilize formatação monetária brasileira (R$) quando apropriado.

    ==================================================
    6. DADOS DA OFICINA
    ==================================================

    Os dados abaixo são disponibilizados para consultas informativas.
    Eles NÃO autorizam a realização manual de cálculos que possuem
    ferramentas próprias.

    {dados_formatados}

    ==================================================
    7. PERGUNTA DO USUÁRIO
    ==================================================

    {pergunta_usuario}

    ==================================================
    INSTRUÇÃO FINAL
    ==================================================

    Antes de responder, verifique se a pergunta exige uma operação
    matemática.

    Se exigir e houver uma ferramenta correspondente, CHAME A FERRAMENTA.

    Somente depois de receber o resultado, formule sua resposta.
    """


    messages = [{'role': 'user', 'content': prompt}]
    
    response = ollama.chat(
        model='gemma4:e4b',
        messages=messages,
        tools=ferramentas,
        options={'temperature': 0.2}
    )
    
    # Adiciona a resposta da Gemma ao contexto
    # apenas desta execução
    messages.append(response.message)

    # Verifica se a Gemma solicitou alguma ferramenta
    if response.message.tool_calls:

        for call in response.message.tool_calls:

            nome_funcao = call.function.name
            argumentos = call.function.arguments

            print("Ferramenta solicitada:", nome_funcao)
            print("Argumentos:", argumentos)

            # Procura a função Python
            funcao = funcoes.get(nome_funcao)

            if funcao is None:
                resultado = {
                    "erro": f"Ferramenta '{nome_funcao}' não encontrada."
                }

            else:
                # Executa a função
                resultado = funcao(**argumentos)

            print("Resultado:", resultado)

            # Devolve o resultado para a Gemma
            messages.append({
                "role": "tool",
                "tool_name": nome_funcao,
                "content": json.dumps(
                    resultado,
                    ensure_ascii=False
                )
            })

        # Segunda chamada da Gemma
        final_response = ollama.chat(
            model="gemma4:e4b",
            messages=messages,
            tools=ferramentas,
            options={
                "temperature": 0.2
            }
        )

        return final_response.message.content

    # Se não precisou de ferramenta
    return response.message.content