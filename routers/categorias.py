from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from database import get_db
from models.categoria import Categoria
from schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaOut
from typing import List
from auth import get_usuario_atual

router = APIRouter(
    prefix="/categorias", 
    tags=["Categorias"]
)

@router.get("/", response_model=List[CategoriaOut])
def listar(
        skip: int = 0, 
        limit: int = 20, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    return db.query(Categoria).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=CategoriaOut)
def buscar(
        id: UUID, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrado")
    return categoria

@router.post("/", response_model=CategoriaOut, status_code=201)
def criar(
        data: CategoriaCreate, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    categoria = Categoria(**data.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

@router.put("/{id}", response_model=CategoriaOut)
def atualizar(
        id: UUID, 
        data: CategoriaUpdate, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrado")
    for campo, valor in data.model_dump().items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria

@router.delete("/{id}", status_code=204)
def deletar(
        id: UUID, 
        db: Session = Depends(get_db), 
        _: str = Depends(get_usuario_atual)
    ):
    categoria = db.query(Categoria).filter(Categoria.id == id).first()
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria não encontrado")
    db.delete(categoria)
    db.commit()