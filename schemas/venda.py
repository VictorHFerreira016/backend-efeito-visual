from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ItemVendaCreate(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float

class ItemVendaOut(ItemVendaCreate):
    id: int

    class Config:
        from_attributes = True

class VendaBase(BaseModel):
    cliente_id: Optional[int] = None
    forma_pagamento: Optional[str] = None
    observacao: Optional[str] = None

class VendaCreate(VendaBase):
    itens: List[ItemVendaCreate]

class VendaOut(VendaBase):
    id: int
    data_venda: datetime
    valor_total: float
    itens: List[ItemVendaOut] = []

    class Config:
        from_attributes = True