from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Fabricante(Base):
    __tablename__ = "fabricantes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String(100), nullable=False)

    produtos = relationship("Produto", back_populates="fabricante")