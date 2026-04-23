from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.produto import Produto
from schemas.produto import ProdutoCreate, ProdutoUpdate, ProdutoOut
from typing import List

router = APIRouter(
    prefix="/produtos", 
    tags=["Produtos"]
)

@router.get("/", response_model=List[ProdutoOut])
def listar(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return db.query(Produto).offset(skip).limit(limit).all()

@router.post("/", response_model=ProdutoOut, status_code=201)
def criar(data: ProdutoCreate, db: Session = Depends(get_db)):
    produto = Produto(**data.model_dump())
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

@router.put("/{id}", response_model=ProdutoOut)
def atualizar(id: int, data: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for campo, valor in data.model_dump().items():
        setattr(produto, campo, valor)
    db.commit()
    db.refresh(produto)
    return produto

@router.delete("/{id}", status_code=204)
def deletar(id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(produto)
    db.commit()