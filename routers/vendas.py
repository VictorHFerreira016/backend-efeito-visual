from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.venda import Venda
from models.item_venda import ItemVenda
from models.produto import Produto
from schemas.venda import VendaCreate, VendaOut
from typing import List

router = APIRouter(prefix="/vendas", tags=["Vendas"])

@router.get("/", response_model=List[VendaOut])
def listar(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Venda).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=VendaOut)
def buscar(id: int, db: Session = Depends(get_db)):
    venda = db.query(Venda).filter(Venda.id == id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return venda

@router.post("/", response_model=VendaOut, status_code=201)
def criar(data: VendaCreate, db: Session = Depends(get_db)):
    valor_total = 0.0
    itens_obj = []

    for item in data.itens:
        produto = db.query(Produto).filter(Produto.id == item.produto_id).first()
        if not produto:
            raise HTTPException(status_code=404, detail=f"Produto {item.produto_id} não encontrado")
        valor_total += item.quantidade * item.preco_unitario
        itens_obj.append(ItemVenda(**item.model_dump()))

    venda = Venda(
        cliente_id=data.cliente_id,
        forma_pagamento=data.forma_pagamento,
        observacao=data.observacao,
        valor_total=valor_total,
        itens=itens_obj
    )
    db.add(venda)
    db.commit()
    db.refresh(venda)
    return venda

@router.delete("/{id}", status_code=204)
def deletar(id: int, db: Session = Depends(get_db)):
    venda = db.query(Venda).filter(Venda.id == id).first()
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    db.delete(venda)
    db.commit()