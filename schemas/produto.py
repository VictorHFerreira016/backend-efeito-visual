from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from uuid import UUID

from schemas.categoria import CategoriaOut
from schemas.fabricante import FabricanteOut
from schemas.fornecedor import FornecedorOut

class ProdutoBase(BaseModel):
    id_categoria: Optional[UUID] = None
    id_fornecedor: Optional[UUID] = None
    id_fabricante: Optional[UUID] = None

    nome: str
    descricao: Optional[str] = None
    preco: float
    quantidade_minima: Optional[int] = 0
    data_validade: Optional[date] = None
    observacoes: Optional[str] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(ProdutoBase):
    pass

class ProdutoOut(ProdutoBase):
    id: UUID
    criado_em: datetime
    atualizado_em: datetime
    categoria: Optional[CategoriaOut] = None
    fabricante: Optional[FabricanteOut] = None
    fornecedor: Optional[FornecedorOut] = None   

    class Config:
        from_attributes = True