import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from core.database import Base


class OrderStatusEnum(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    cancelled = "cancelled"


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("client.id"), nullable=False)
    status = Column(Enum(OrderStatusEnum), default=OrderStatusEnum.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    client = relationship("Client")
    products = relationship(
        "OrderProduct", back_populates="order", cascade="all, delete"
    )


class OrderProduct(Base):
    __tablename__ = "order_products"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    order = relationship("Order", back_populates="products")
    product = relationship("Product")
