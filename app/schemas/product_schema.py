from datetime import date
from typing import Optional

from pydantic import BaseModel, computed_field


class ProductRequest(BaseModel):
    description: str
    sale_value: float
    barcode: str
    section: str
    initial_stock: int
    expiration_date: Optional[date] = None
    image: Optional[str] = None
    category: str


class ProductResponse(ProductRequest):
    id: int

    @computed_field
    @property
    def availability(self) -> bool:
        return self.initial_stock > 0

    class Config:
        from_attributes = True
