from pydantic import BaseModel
from uuid import UUID

class FabricanteBase(BaseModel):
    nome: str

class FabricanteCreate(FabricanteBase):
    pass

class FabricanteUpdate(FabricanteBase):
    pass

class FabricanteOut(FabricanteBase):
    id: UUID

    class Config:
        from_attributes = True