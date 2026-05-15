from sqlalchemy import Column, String, UUID
from sqlalchemy.orm import relationship
import uuid
from database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    nome = Column(String(100), nullable=False)

    produtos = relationship("Produto", back_populates="categoria")