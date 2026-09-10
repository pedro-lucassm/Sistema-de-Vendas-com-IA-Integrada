# Puxando a biblioteca do FASTAPI e a regra de cors
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Ferramenta do FastAPI que permite o front fazer requisições para o back

#Puxando funçoes
from vendas import listar_vendas

app = FastAPI() # Inicia o servidor

# Configuração que autoriza o JavaScript a conversar com o Python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # Qualquer servidor pode fazer requisições
    allow_credentials=True, # Autoriza metodos HTTP (GET, POST, PUT, DELETE)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas
@app.get("/vendas")
def get_vendas():
    return listar_vendas()