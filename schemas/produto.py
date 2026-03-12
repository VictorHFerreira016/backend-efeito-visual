from pydantic import BaseModel
from typing import Optional

class ProdutoBase(BaseModel):
    nome: str
    categoria: Optional[str] = None
    quantidade: int = 0
    preco: float
    fornecedor: Optional[str] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id: int

    class Config:
        from_attributes = True