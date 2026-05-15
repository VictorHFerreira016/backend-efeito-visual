from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.estoque import Estoque
from schemas.estoque import EstoqueCreate, EstoqueUpdate, EstoqueOut
from typing import List
from uuid import UUID
from auth import get_usuario_atual

router = APIRouter(
    prefix="/estoques", 
    tags=["Estoques"]
)

@router.get("/", response_model=List[EstoqueOut])
def listar(
        skip: int = 0, 
        limit: int = 20, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    return db.query(Estoque).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=EstoqueOut)
def buscar(
        id: UUID, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    estoque = db.query(Estoque).filter(Estoque.id == id).first()
    if not estoque:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    return estoque

@router.post("/", response_model=EstoqueOut, status_code=201)
def criar(
        data: EstoqueCreate, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    estoque = Estoque(**data.model_dump())
    db.add(estoque)
    db.commit()
    db.refresh(estoque)
    return estoque

@router.put("/{id}", response_model=EstoqueOut)
def atualizar(
        id: UUID, 
        data: EstoqueUpdate, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    estoque = db.query(Estoque).filter(Estoque.id == id).first()
    if not estoque:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    for campo, valor in data.model_dump().items():
        setattr(estoque, campo, valor)
    db.commit()
    db.refresh(estoque)
    return estoque

@router.delete("/{id}", status_code=204)
def deletar(
        id: UUID, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    estoque = db.query(Estoque).filter(Estoque.id == id).first()
    if not estoque:
        raise HTTPException(status_code=404, detail="Estoque não encontrado")
    db.delete(estoque)
    db.commit()