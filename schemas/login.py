from pydantic import BaseModel

class LoginBase(BaseModel):
    email: str
    senha: str

class LoginCreate(LoginBase):
    pass

class LoginUpdate(LoginBase):
    pass

class LoginOut(LoginBase):
    id: int

    class Config:
        from_attributes = True