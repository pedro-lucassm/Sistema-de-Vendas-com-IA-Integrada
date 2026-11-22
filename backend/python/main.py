# Puxando a biblioteca do FASTAPI e a regra de cors
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

#Puxando funçoes
from vendas import criar_venda,listar_vendas, atualizar_venda, excluir_venda
from clientes import criar_cliente, listar_clientes
from produtos import criar_produto, listar_produtos
from main_AI import resposta_ia

app = FastAPI()

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

class ProdutoCreateSchema(BaseModel):
    nome_produto: str
    categoria: str
    preco_custo: float
    preco_venda: float
    estoque: int

class ItemVendaCreateSchema(BaseModel):
    id_produto: int
    quantidade: int
    preco_unitario: float
    subtotal: float

class VendaCreateSchema(BaseModel):
    id_cliente: int
    data_venda: datetime
    valor_total: float
    itens: List[ItemVendaCreateSchema]

VendaCreateSchema.model_rebuild()

class PerguntaRequest(BaseModel):
    pergunta: str

# Rotas

# Get
@app.get("/vendas")
def get_vendas():
    return listar_vendas()

@app.get("/clientes")
def get_clientes():
    return listar_clientes()

@app.get("/produtos")
def get_produtos():
    return listar_produtos()

# Post
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

@app.post("/cadastro_produtos")
def post_produto(dados: ProdutoCreateSchema):
    criar_produto(
        nome_produto=dados.nome_produto,
        categoria=dados.categoria,
        preco_custo=dados.preco_custo,
        preco_venda=dados.preco_venda,
        estoque=dados.estoque
    )
    return {"mensagem": "Cliente cadastrado com sucesso!"}

@app.post("/cadastro_vendas")
def post_venda(dados: VendaCreateSchema):
    criar_venda(dados)
    return {"mensagem": "Venda cadastrada com sucesso!"}

@app.post("/perguntar")
def consultar_ia(dados: PerguntaRequest):
    resposta = resposta_ia(dados.pergunta)
    return {"resposta": resposta}

# Delete
@app.delete("/vendas/{id_venda}")
def deletar_venda(id_venda: int):
    return excluir_venda(id_venda)