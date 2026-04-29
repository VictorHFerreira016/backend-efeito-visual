from pydantic import BaseModel

class LoginBase(BaseModel):
    email: str
    senha: str

class LoginCreate(LoginBase):
    pass

class LoginUpdate(LoginBase):
    pass

class LoginOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True