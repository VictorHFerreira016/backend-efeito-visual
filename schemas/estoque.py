from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class EstoqueBase(BaseModel):
    id_produto: UUID
    quantidade: int
    preco_pago: float

class EstoqueCreate(EstoqueBase):
    pass

class EstoqueUpdate(BaseModel):
    id_produto: Optional[UUID]
    quantidade: Optional[int]
    preco_pago: Optional[float]

class EstoqueOut(EstoqueBase):
    id: UUID

    class Config:
        from_attributes = True