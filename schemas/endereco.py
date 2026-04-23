from pydantic import BaseModel
from typing import Optional

class EnderecoBase(BaseModel):
    cliente_id: int
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    pais: Optional[str] = None
 
class EnderecoCreate(EnderecoBase):
    pass

class EnderecoUpdate(EnderecoBase):
    pass

class EnderecoOut(EnderecoBase):
    id: int

    class Config:
        from_attributes = True