from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class TelefoneBase(BaseModel):
    numero: str
    tipo: Optional[str] = None

class TelefoneCreate(TelefoneBase):
    pass

class TelefoneUpdate(TelefoneBase):
    pass

class TelefoneOut(TelefoneBase):
    id: UUID

    class Config:
        from_attributes = True