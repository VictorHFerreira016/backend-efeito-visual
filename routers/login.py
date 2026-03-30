from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.login import Login
from schemas.login import LoginCreate, LoginUpdate, LoginOut
from typing import List

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.get("/", response_model=List[LoginOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Login).all()

@router.post("/", response_model=LoginOut, status_code=201)
def criar(data: LoginCreate, db: Session = Depends(get_db)):
    login = Login(**data.model_dump())
    db.add(login)
    db.commit()
    db.refresh(login)
    return login

@router.put("/{id}", response_model=LoginOut)
def atualizar(id: int, data: LoginUpdate, db: Session = Depends(get_db)):
    login = db.query(Login).filter(Login.id == id).first()
    if not login:
        raise HTTPException(status_code=404, detail="Login não encontrado")
    for campo, valor in data.model_dump().items():
        setattr(login, campo, valor)
    db.commit()
    db.refresh(login)
    return login

@router.delete("/{id}", status_code=204)
def deletar(id: int, db: Session = Depends(get_db)):
    login = db.query(Login).filter(Login.id == id).first()
    if not login:
        raise HTTPException(status_code=404, detail="Login não encontrado")
    db.delete(login)
    db.commit()