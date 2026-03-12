from pydantic import BaseModel
from typing import Optional

class ServicoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float
    duracao: Optional[str] = None

class ServicoCreate(ServicoBase):
    pass

class ServicoUpdate(ServicoBase):
    pass

class ServicoOut(ServicoBase):
    id: int

    class Config:
        from_attributes = True