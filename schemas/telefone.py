from pydantic import BaseModel
from typing import Optional

class TelefoneBase(BaseModel):
    cliente_id: int
    numero: str
    tipo: Optional[str] = None

class TelefoneCreate(TelefoneBase):
    pass

class TelefoneUpdate(TelefoneBase):
    pass

class TelefoneOut(TelefoneBase):
    id: int

    class Config:
        from_attributes = True