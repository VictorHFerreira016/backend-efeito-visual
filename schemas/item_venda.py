from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ItemVendaBase(BaseModel):
    id_produto: Optional[UUID] = None
    id_servico: Optional[UUID] = None
    id_venda: UUID
    quantidade: int
    preco_unitario: float

class ItemVendaCreate(ItemVendaBase):
    pass

class ItemVendaUpdate(ItemVendaBase):
    pass

class ItemVendaOut(ItemVendaBase):
    id: UUID

    class Config:
        from_attributes = True