from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models.produto import Produto
from models.estoque import Estoque
from sqlalchemy import func
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoOut
from typing import List
from uuid import UUID
from auth import get_usuario_atual

router = APIRouter(
    prefix="/produtos", 
    tags=["Produtos"]
)

# ----------------------
# - SCHEMAS EXCLUSIVOS -
# ----------------------
class ProdutoEstoqueBaixoOut(BaseModel):
    id: UUID
    nome: str
    quantidade_minima: int
    quantidade_atual: int
 
 
class EstoqueResumoItemOut(BaseModel):
    id_produto: UUID
    nome_produto: str
    quantidade_total: int
    valor_investido: float
    lote_mais_antigo: Optional[datetime]
    num_lotes: int

# ---------------------------------------------------------------------------
# ATENÇÃO — rotas estáticas DEVEM vir antes de /{id}
# Se /{id} vier primeiro, o FastAPI vai tentar converter "estoque" como UUID
# e retornar 422 antes de chegar nas rotas corretas.
# ---------------------------------------------------------------------------

# GET /produtos/estoque/baixo
# Lista produtos com estoque abaixo do mínimo definido em quantidade_minima
@router.get("/estoque/baixo", response_model=List[ProdutoEstoqueBaixoOut])
def estoque_baixo(
    db: Session = Depends(get_db),
    _: str = Depends(get_usuario_atual),
):
    # Subquery: soma de estoque disponível por produto
    subq = (
        db.query(
            Estoque.id_produto,
            func.sum(Estoque.quantidade).label("total"),
        )
        .group_by(Estoque.id_produto)
        .subquery()
    )
 
    resultados = (
        db.query(Produto, subq.c.total)
        .outerjoin(subq, Produto.id == subq.c.id_produto)
        .filter(
            Produto.quantidade_minima > 0,
            # Produto sem nenhum lote OR lotes insuficientes
            (subq.c.total == None) | (subq.c.total < Produto.quantidade_minima),
        )
        .order_by(Produto.nome)
        .all()
    )
 
    return [
        ProdutoEstoqueBaixoOut(
            id=produto.id,
            nome=produto.nome,
            quantidade_minima=produto.quantidade_minima or 0,
            quantidade_atual=int(total or 0),
        )
        for produto, total in resultados
    ]


# GET /produtos/estoque/resumo
# Retorna um resumo de estoque para todos os produtos:
# quantidade total, valor investido em lotes, lote mais antigo e número de lotes
@router.get("/estoque/resumo", response_model=List[EstoqueResumoItemOut])
def estoque_resumo(
    db: Session = Depends(get_db),
    _: str = Depends(get_usuario_atual),
):
    resultados = (
        db.query(
            Produto.id,
            Produto.nome,
            func.coalesce(func.sum(Estoque.quantidade), 0).label("quantidade_total"),
            # Valor investido = soma de (quantidade * preco_pago) por lote
            func.coalesce(
                func.sum(Estoque.quantidade * Estoque.preco_pago), 0
            ).label("valor_investido"),
            func.min(Estoque.criado_em).label("lote_mais_antigo"),
            func.count(Estoque.id).label("num_lotes"),
        )
        .outerjoin(Estoque, Produto.id == Estoque.id_produto)
        .group_by(Produto.id, Produto.nome)
        .order_by(Produto.nome)
        .all()
    )
 
    return [
        EstoqueResumoItemOut(
            id_produto=r.id,
            nome_produto=r.nome,
            quantidade_total=int(r.quantidade_total),
            valor_investido=round(float(r.valor_investido), 2),
            lote_mais_antigo=r.lote_mais_antigo,
            num_lotes=r.num_lotes,
        )
        for r in resultados
    ]

# ---------------------------------------------------------------------------
# Rotas CRUD padrão — vêm depois das rotas estáticas
# ---------------------------------------------------------------------------

@router.get("/", response_model=List[ProdutoOut])
def listar(
        skip: int = 0, 
        limit: int = 20, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    return (
        db.query(Produto)
        .options(joinedload(Produto.categoria), joinedload(Produto.fabricante), joinedload(Produto.fornecedor))
        .offset(skip)
        .limit(limit)
        .all()
    )

@router.get("/{id}", response_model=ProdutoOut)
def buscar(
        id: UUID, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@router.post("/", response_model=ProdutoOut, status_code=201)
def criar(
        data: ProdutoCreate, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    produto = Produto(**data.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

@router.put("/{id}", response_model=ProdutoOut)
def atualizar(
        id: UUID, 
        data: ProdutoUpdate, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for campo, valor in data.model_dump().items():
        setattr(produto, campo, valor)
    db.commit()
    db.refresh(produto)
    return produto

@router.delete("/{id}", status_code=204)
def deletar(
        id: UUID, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()