from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.order_and_orderProduct_model import (
    Order,
    OrderProduct,
    OrderStatusEnum,
)
from app.models.product_model import Product
from app.schemas.order_and_orderProduct_schema import (
    OrderRequest,
    OrderResponse,
    OrderUpdateRequest,
)
from core.dependencies import get_db
from core.security import get_current_admin_user, get_current_user

router = APIRouter(prefix="/orders")


@router.get(
    "",
    response_model=List[OrderResponse],
    dependencies=(Depends(get_current_user)),
)
def get_orders(
    client_id: Optional[int] = None,
    status: Optional[OrderStatusEnum] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Order)

    if client_id:
        query = query.filter(Order.client_id == client_id)
    if status:
        query = query.filter(Order.status == status)
    if start_date:
        query = query.filter(Order.created_at >= start_date)
    if end_date:
        query = query.filter(Order.created_at <= end_date)

    return query.all()


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=(Depends(get_current_user)),
)
def create_order(order_request: OrderRequest, db: Session = Depends(get_db)):
    order = Order(client_id=order_request.client_id)
    total = 0

    for item in order_request.products:
        product = (
            db.query(Product).filter(Product.id == item.product_id).first()
        )

        if not product:
            raise HTTPException(status_code=404, detail="Product not found.")

        if product.initial_stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Insufficient stock for product: {product.description}"
                ),
            )

        product.initial_stock -= item.quantity

        subtotal = item.quantity * product.sale_value
        order_product = OrderProduct(
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.sale_value,
            subtotal=subtotal,
        )

        order.products.append(order_product)
        total += subtotal

    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get(
    "/{id}",
    response_model=OrderResponse,
    dependencies=(Depends(get_current_user)),
)
def get_order_by_id(id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    return order


@router.put(
    "/{id}",
    response_model=OrderResponse,
    dependencies=(Depends(get_current_admin_user)),
)
def update_order(
    id: int, order_request: OrderUpdateRequest, db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    order.status = order_request.status

    db.commit()
    db.refresh(order)
    return order


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=(Depends(get_current_admin_user)),
)
def delete_order(id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found.")

    db.delete(order)
    db.commit
