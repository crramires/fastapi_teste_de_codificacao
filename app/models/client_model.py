from sqlalchemy import Column, Integer, String

from core.database import Base


class Client(Base):
    __tablename__ = "client"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), nullable=False)
    email = Column(String(30), nullable=False, unique=True)
    cpf = Column(String(11), nullable=False, unique=True)
