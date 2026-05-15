from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.venda import Venda
from models.item_venda import ItemVenda
from models.produto import Produto
from models.servico import Servico
from models.estoque import Estoque
from schemas.venda import VendaCreate, VendaOut
from typing import List, cast
from uuid import UUID
from auth import get_usuario_atual

router = APIRouter(prefix="/vendas", tags=["Vendas"])


@router.get("/", response_model=List[VendaOut])
def listar(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    _: str = Depends(get_usuario_atual),
):
    return db.query(Venda).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=VendaOut)
def buscar(
    id: UUID,
    db: Session = Depends(get_db),
    _: str = Depends(get_usuario_atual),
):
    venda = db.query(Venda).filter(Venda.id == id).first()
    if venda is None:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda


@router.post("/", response_model=VendaOut, status_code=201)
def criar(
    data: VendaCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_usuario_atual),
):
    valor_total = 0.0
    itens_obj = []

    for item in data.itens:
        if item.id_produto is not None:
            # Verifica se o produto existe
            produto = db.query(Produto).filter(Produto.id == item.id_produto).first()
            if produto is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Produto {item.id_produto} não encontrado",
                )

            # Busca os lotes do produto em ordem FIFO (mais antigo primeiro)
            lotes = (
                db.query(Estoque)
                .filter(
                    Estoque.id_produto == item.id_produto,
                    Estoque.quantidade > 0,
                )
                .order_by(Estoque.criado_em.asc())
                .all()
            )

            # Verifica se o estoque total é suficiente
            # int() converte Column[int] → int puro para comparações seguras
            total_disponivel: int = sum(cast(int, lote.quantidade) for lote in lotes)
            if item.quantidade > total_disponivel:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Estoque insuficiente para o produto {item.id_produto}. "
                        f"Solicitado: {item.quantidade}, disponível: {total_disponivel}"
                    ),
                )

            # Debita os lotes em ordem FIFO
            restante: int = item.quantidade
            for lote in lotes:
                if restante <= 0:
                    break
                lote_qty: int = cast(int, lote.quantidade)
                if lote_qty >= restante:
                    setattr(lote, "quantidade", lote_qty - restante)
                    restante = 0
                else:
                    restante -= lote_qty
                    setattr(lote, "quantidade", 0)

        else:
            # Serviço: apenas valida que existe
            servico = db.query(Servico).filter(Servico.id == item.id_servico).first()
            if servico is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Serviço {item.id_servico} não encontrado",
                )

        valor_total += item.quantidade * item.preco_unitario
        itens_obj.append(ItemVenda(**item.model_dump()))

    venda = Venda(
        id_cliente=data.id_cliente,
        forma_pagamento=data.forma_pagamento,
        observacao=data.observacao,
        valor_total=valor_total,
        itens=itens_obj,
    )
    db.add(venda)
    db.commit()
    db.refresh(venda)
    return venda


@router.delete("/{id}", status_code=204)
def deletar(
    id: UUID,
    db: Session = Depends(get_db),
    _: str = Depends(get_usuario_atual),
):
    venda = db.query(Venda).filter(Venda.id == id).first()
    if venda is None:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    db.delete(venda)
    db.commit()
    return