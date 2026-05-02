from pydantic import BaseModel, model_validator
from typing import Optional, List
from datetime import datetime

class ItemVendaCreate(BaseModel):
    produto_id: Optional[int] = None
    servico_id: Optional[int] = None
    quantidade: int
    preco_unitario: float

    @model_validator(mode="after")
    def validar_produto_ou_servico(self):
        tem_produto = self.produto_id is not None
        tem_servico = self.servico_id is not None
        if tem_produto == tem_servico:  # ambos ou nenhum
            raise ValueError("Informe produto_id OU servico_id, não ambos e não nenhum")
        return self

class ItemVendaOut(BaseModel):
    id: int
    produto_id: Optional[int] = None
    servico_id: Optional[int] = None
    quantidade: int
    preco_unitario: float

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