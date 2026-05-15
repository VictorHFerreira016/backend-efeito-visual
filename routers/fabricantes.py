from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.fabricante import Fabricante
from schemas.fabricante import FabricanteCreate, FabricanteUpdate, FabricanteOut
from typing import List
from uuid import UUID
from auth import get_usuario_atual

router = APIRouter(
    prefix="/fabricantes", 
    tags=["Fabricantes"]
)

@router.get("/", response_model=List[FabricanteOut])
def listar(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    return db.query(Fabricante).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=FabricanteOut)
def buscar(id: UUID, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    fabricante = db.query(Fabricante).filter(Fabricante.id == id).first()
    if not fabricante:
        raise HTTPException(status_code=404, detail="Fabricante não encontrado")
    return fabricante

@router.post("/", response_model=FabricanteOut, status_code=201)
def criar(data: FabricanteCreate, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    fabricante = Fabricante(**data.model_dump())
    db.add(fabricante)
    db.commit()
    db.refresh(fabricante)
    return fabricante

@router.put("/{id}", response_model=FabricanteOut)
def atualizar(id: UUID, data: FabricanteUpdate, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    fabricante = db.query(Fabricante).filter(Fabricante.id == id).first()
    if not fabricante:
        raise HTTPException(status_code=404, detail="Fabricante não encontrado")
    for campo, valor in data.model_dump().items():
        setattr(fabricante, campo, valor)
    db.commit()
    db.refresh(fabricante)
    return fabricante

@router.delete("/{id}", status_code=204)
def deletar(id: UUID, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    fabricante = db.query(Fabricante).filter(Fabricante.id == id).first()
    if not fabricante:
        raise HTTPException(status_code=404, detail="Fabricante não encontrado")
    db.delete(fabricante)
    db.commit()