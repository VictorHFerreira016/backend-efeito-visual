from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.cliente import Cliente
from models.telefone import Telefone
from models.endereco import Endereco
from schemas.cliente import ClienteCreate, ClienteUpdate, ClienteOut
from typing import List
from auth import get_usuario_atual

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=List[ClienteOut])
def listar(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    return db.query(Cliente).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=ClienteOut)
def buscar(id: int, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente

@router.post("/", response_model=ClienteOut, status_code=201)
def criar(data: ClienteCreate, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    cliente = Cliente(
        **data.model_dump(exclude={"enderecos", "telefones"}), 
        enderecos=[Endereco(**e.model_dump()) for e in data.enderecos], 
        telefones=[Telefone(**t.model_dump()) for t in data.telefones]
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

@router.put("/{id}", response_model=ClienteOut)
def atualizar(id: int, data: ClienteUpdate, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    for campo, valor in data.model_dump(exclude={"enderecos", "telefones"}).items():
        setattr(cliente, campo, valor)
    db.commit()
    db.refresh(cliente)
    return cliente

@router.delete("/{id}", status_code=204)
def deletar(id: int, db: Session = Depends(get_db), _: str = Depends(get_usuario_atual)):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    db.delete(cliente)
    db.commit()