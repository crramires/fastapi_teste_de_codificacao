from datetime import datetime
from typing import List

from pydantic import BaseModel


class OrderItemRequest(BaseModel):
    product_id: int
    quantity: int


class OrderRequest(BaseModel):
    client_id: int
    products: List[OrderItemRequest]


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    client_id: int
    status: str
    created_at: datetime
    products: List[OrderItemResponse]

    class Config:
        from_attributes = True


class OrderUpdateRequest(BaseModel):
    status: str
