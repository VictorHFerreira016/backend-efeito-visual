from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.servico import Servico
from schemas.servico import ServicoCreate, ServicoUpdate, ServicoOut
from typing import List
from auth import get_usuario_atual

router = APIRouter(
    prefix="/servicos", 
    tags=["Serviços"]
)

@router.get("/", response_model=List[ServicoOut])
def listar(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    return db.query(Servico).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=ServicoOut)
def buscar(id: int, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    servico = db.query(Servico).filter(Servico.id == id).first()
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    return servico

@router.post("/", response_model=ServicoOut, status_code=201)
def criar(data: ServicoCreate, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    servico = Servico(**data.model_dump())
    db.add(servico)
    db.commit()
    db.refresh(servico)
    return servico

@router.put("/{id}", response_model=ServicoOut)
def atualizar(id: int, data: ServicoUpdate, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    servico = db.query(Servico).filter(Servico.id == id).first()
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    for campo, valor in data.model_dump().items():
        setattr(servico, campo, valor)
    db.commit()
    db.refresh(servico)
    return servico

@router.delete("/{id}", status_code=204)
def deletar(id: int, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    servico = db.query(Servico).filter(Servico.id == id).first()
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    db.delete(servico)
    db.commit()