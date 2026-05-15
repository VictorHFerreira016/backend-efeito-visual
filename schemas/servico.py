from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import time

class ServicoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    duracao: Optional[time] = None

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(ServicoBase):
    pass

class ServicoOut(ServicoBase):
    id: UUID

    class Config:
        from_attributes = True