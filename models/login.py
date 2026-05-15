from sqlalchemy import Column, UUID, String
from database import Base
import uuid

class Login(Base):
    __tablename__ = "login"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    email = Column(String(200), nullable=False)
    senha = Column(String(200), nullable=False)