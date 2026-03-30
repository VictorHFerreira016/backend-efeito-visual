from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Login(Base):
    __tablename__ = "login"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)