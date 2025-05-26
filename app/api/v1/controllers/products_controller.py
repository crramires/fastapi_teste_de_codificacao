from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.product_model import Product
from app.schemas.product_schema import ProductRequest, ProductResponse
from core.dependencies import get_db
from core.security import get_current_admin_user, get_current_user

router = APIRouter(prefix="/products")


@router.get(
    "",
    response_model=List[ProductResponse],
    dependencies=(Depends(get_current_user)),
)
def get_products(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    category: Optional[str] = None,
    section: Optional[str] = None,
    value_min: Optional[float] = None,
    value_max: Optional[float] = None,
    availability: Optional[bool] = None,
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))
    if section:
        query = query.filter(Product.section.ilike(f"%{section}%"))
    if value_min is not None:
        query = query.filter(Product.sale_value >= value_min)
    if value_max is not None:
        query = query.filter(Product.sale_value <= value_max)

    if availability is not None:
        if availability:
            query = query.filter(Product.initial_stock > 0)
        else:
            query = query.filter(Product.initial_stock <= 0)

    products = query.offset(skip).limit(limit).all()
    return products


@router.get(
    "/{id}",
    response_model=ProductResponse,
    dependencies=(Depends(get_current_user)),
)
def get_product_by_id(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=(Depends(get_current_user)),
)
def create_product(
    product_request: ProductRequest, db: Session = Depends(get_db)
):
    existing_product = (
        db.query(Product)
        .filter(Product.barcode == product_request.barcode)
        .first()
    )

    if existing_product:
        raise HTTPException(status_code=400, detail="Registered barcode")
    try:
        product = Product(**product_request.model_dump())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Databse error while creating product"
        )


@router.put(
    "/{id}",
    response_model=ProductResponse,
    dependencies=(Depends(get_current_user)),
)
def update_product(
    id: int, product_request: ProductRequest, db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product not found.")

    try:
        for attr, value in product_request.model_dump().items():
            setattr(product, attr, value)

        db.commit()
        db.refresh(product)
        return product

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Databse error while updating product."
        )


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=(Depends(get_current_admin_user)),
)
def delete_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=400, detail="Product not found")
    try:
        db.delete(product)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Databse error whiel deleting product"
        )
