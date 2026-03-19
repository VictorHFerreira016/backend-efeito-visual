from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routers import servicos, produtos, clientes, vendas

app = FastAPI(title="efeito_visual")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(produtos.router)
app.include_router(servicos.router)
app.include_router(clientes.router)
app.include_router(vendas.router)