from pydantic import BaseModel
from uuid import UUID

class FornecedorBase(BaseModel):
    nome: str

class FornecedorCreate(FornecedorBase):
    pass

class FornecedorUpdate(FornecedorBase):
    pass

class FornecedorOut(FornecedorBase):
    id: UUID

    class Config:
        from_attributes = True