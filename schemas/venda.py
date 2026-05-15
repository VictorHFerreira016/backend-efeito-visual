from pydantic import BaseModel, model_validator
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class ItemVendaCreate(BaseModel):
    id_produto: Optional[UUID] = None 
    id_servico: Optional[UUID] = None
    quantidade: int
    preco_unitario: float

    @model_validator(mode="after")
    def validar_produto_ou_servico(self):
        tem_produto = self.id_produto is not None
        tem_servico = self.id_servico is not None
        if tem_produto == tem_servico:  # ambos ou nenhum
            raise ValueError("Informe id_produto OU id_servico, não ambos e não nenhum")
        return self

class ItemVendaOut(BaseModel):
    id: UUID
    id_produto: Optional[UUID] = None
    id_servico: Optional[UUID] = None
    quantidade: int
    preco_unitario: float

    class Config:
        from_attributes = True

class VendaBase(BaseModel):
    id_cliente: Optional[UUID] = None
    forma_pagamento: Optional[str] = None
    observacao: Optional[str] = None

class VendaCreate(VendaBase):
    itens: List[ItemVendaCreate]

class VendaOut(VendaBase):
    id: UUID
    criado_em: datetime
    valor_total: float
    itens: List[ItemVendaOut] = []

    class Config:
        from_attributes = True