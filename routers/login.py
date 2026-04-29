# código novo completo
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from models.login import Login
from schemas.login import LoginCreate, LoginUpdate, LoginOut
from auth import hash_senha, verificar_senha, criar_token, get_usuario_atual

router = APIRouter(prefix="/login", tags=["Login"])

@router.get("/me", response_model=LoginOut)
def me(email: str = Depends(get_usuario_atual), db: Session = Depends(get_db)):
    login = db.query(Login).filter(Login.email == email).first()
    if not login:
        raise HTTPException(status_code=404, detail="Login não encontrado")
    return login

@router.post("/register", response_model=LoginOut, status_code=201)
def registrar(data: LoginCreate = Depends(get_usuario_atual), db: Session = Depends(get_db)):
    existente = db.query(Login).filter(Login.email == data.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    login = Login(email=data.email, senha=hash_senha(data.senha))
    db.add(login)
    db.commit()
    db.refresh(login)
    return login

@router.post("/token")
def autenticar(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    login = db.query(Login).filter(Login.email == form.username).first()
    if not login or not verificar_senha(form.password, str(login.senha)):
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")
    token = criar_token({"sub": login.email})
    return {"access_token": token, "token_type": "bearer"}

@router.put("/{id}", response_model=LoginOut)
def atualizar(id: int, data: LoginUpdate, db: Session = Depends(get_db)):
    login = db.query(Login).filter(Login.id == id).first()
    if not login:
        raise HTTPException(status_code=404, detail="Login não encontrado")
    setattr(login, "email", data.email)
    setattr(login, "senha", hash_senha(data.senha))
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