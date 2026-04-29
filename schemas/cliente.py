from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from schemas.endereco import EnderecoCreate, EnderecoOut
from schemas.telefone import TelefoneCreate, TelefoneOut

class ClienteBase(BaseModel):
    nome: str
    cpf: Optional[str] = None
    rg: Optional[str] = None
    data_nascimento: Optional[date] = None
    sexo: Optional[str] = None

class ClienteCreate(ClienteBase):
    enderecos: List[EnderecoCreate] = []
    telefones: List[TelefoneCreate] = []

class ClienteUpdate(ClienteBase):
    enderecos: List[EnderecoCreate] = []
    telefones: List[TelefoneCreate] = []

class ClienteOut(ClienteBase):
    id: int
    enderecos: List[EnderecoOut] = []
    telefones: List[TelefoneOut] = []

    class Config:
        from_attributes = True