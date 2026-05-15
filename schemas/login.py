from pydantic import BaseModel
from uuid import UUID

class LoginBase(BaseModel):
    email: str
    senha: str

class LoginCreate(LoginBase):
    pass

class LoginUpdate(LoginBase):
    pass

class LoginOut(BaseModel):
    id: UUID
    email: str

    class Config:
        from_attributes = True