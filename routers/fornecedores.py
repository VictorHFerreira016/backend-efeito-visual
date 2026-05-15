from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.fornecedor import Fornecedor
from schemas.fornecedor import FornecedorCreate, FornecedorUpdate, FornecedorOut
from typing import List
from uuid import UUID
from auth import get_usuario_atual

router = APIRouter(
    prefix="/fornecedores", 
    tags=["Fornecedores"]
)

@router.get("/", response_model=List[FornecedorOut])
def listar(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    return db.query(Fornecedor).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=FornecedorOut)
def buscar(id: UUID, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return fornecedor

@router.post("/", response_model=FornecedorOut, status_code=201)
def criar(data: FornecedorCreate, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    fornecedor = Fornecedor(**data.model_dump())
    db.add(fornecedor)
    db.commit()
    db.refresh(fornecedor)
    return fornecedor

@router.put("/{id}", response_model=FornecedorOut)
def atualizar(id: UUID, data: FornecedorUpdate, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    for campo, valor in data.model_dump().items():
        setattr(fornecedor, campo, valor)
    db.commit()
    db.refresh(fornecedor)
    return fornecedor

@router.delete("/{id}", status_code=204)
def deletar(id: UUID, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    fornecedor = db.query(Fornecedor).filter(Fornecedor.id == id).first()
    if not fornecedor:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    db.delete(fornecedor)
    db.commit()