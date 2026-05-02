import os
import logging
import traceback

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from database import Base, engine
from routers import servicos, produtos, clientes, vendas, login

logger = logging.getLogger(__name__)

app = FastAPI(title="efeito_visual")

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"SQLAlchemy error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": f"Erro no banco de dados: {str(exc)}"}
    )

@app.exception_handler(Exception)
async def generic_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": f"Erro interno: {str(exc)}"}
    )

ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(produtos.router)
app.include_router(servicos.router)
app.include_router(clientes.router)
app.include_router(vendas.router)
app.include_router(login.router)