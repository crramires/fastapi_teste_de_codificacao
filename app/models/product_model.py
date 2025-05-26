from sqlalchemy import (
    Column,
    Date,
    Float,
    Integer,
    String,
    Text,
    UniqueConstraint,
)

from core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String(255), nullable=False)
    sale_value = Column(Float, nullable=False)
    barcode = Column(String(255), nullable=False)
    section = Column(String(50), nullable=False, unique=True)
    initial_stock = Column(Integer, nullable=False, default=0)
    expiration_date = Column(Date, nullable=True)
    image = Column(Text, nullable=True)
    category = Column(String(100), nullable=False)

    __table_args__ = (UniqueConstraint("barcode", name="uq_barcode"),)
