# Puxando a biblioteca do FASTAPI e a regra de cors
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Ferramenta do FastAPI que permite o front fazer requisições para o back
from pydantic import BaseModel
from typing import Optional

#Puxando funçoes
from vendas import criar_venda,listar_vendas, atualizar_venda, excluir_venda
from clientes import criar_cliente

app = FastAPI() # Inicia o servidor

# Configuração que autoriza o JavaScript a conversar com o Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Qualquer servidor pode fazer requisições
    allow_credentials=True, # Autoriza metodos HTTP (GET, POST, PUT, DELETE)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema para validar o JSON do formulario
class ClienteCreateSchema(BaseModel):
    nome_cliente: str
    tipo_doc: str
    cpf_cnpj: str
    telefone: str
    email: Optional[str] = None
    cep: Optional[str] = None
    rua: Optional[str] = None
    numero: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None

# Rotas
@app.get("/vendas")
def get_vendas():
    return listar_vendas()

@app.post("/cadastro_clientes")
def post_cliente(dados: ClienteCreateSchema):
    criar_cliente(
        nome_cliente=dados.nome_cliente,
        tipo_doc=dados.tipo_doc,
        cpf_cnpj=dados.cpf_cnpj,
        telefone=dados.telefone,
        email=dados.email,
        cep=dados.cep,
        rua=dados.rua,
        numero=dados.numero,
        cidade=dados.cidade,
        estado=dados.estado
    )
    return {"mensagem": "Cliente cadastrado com sucesso!"}
