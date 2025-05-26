from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.client_model import Client
from app.schemas.client_schema import ClientRequest, ClientResponse
from core.dependencies import get_db
from core.security import get_current_admin_user, get_current_user

router = APIRouter(prefix="/clients")


# List all clients
@router.get(
    "",
    response_model=List[ClientResponse],
    dependencies=[Depends(get_current_user)],
)
def get_client(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    name: Optional[str] = None,
    email: Optional[str] = None,
):
    query = db.query(Client)

    if name:
        query = query.filter(Client.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))

    client = query.offset(skip).limit(limit).all()

    return client


# List a client by id
@router.get(
    "/{id}",
    response_model=ClientResponse,
    dependencies=[Depends(get_current_user)],
)
def get_client_by_id(id: int, db: Session = Depends(get_db)) -> ClientResponse:
    client = db.get(Client, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


# Create a new client
@router.post(
    "",
    response_model=ClientResponse,
    status_code=201,
    dependencies=[Depends(get_current_user)],
)
def create_client(
    client_request: ClientRequest, db: Session = Depends(get_db)
) -> ClientResponse:
    try:
        client = Client(**client_request.model_dump())
        db.add(client)
        db.commit()
        db.refresh(client)
        return client
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Client with this email or CPF already exists.",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Database error while creating client."
        )


# Update a client
@router.put(
    "/{id}",
    response_model=ClientResponse,
    status_code=200,
    dependencies=[Depends(get_current_user)],
)
def update_client(
    id: int, client_request: ClientRequest, db: Session = Depends(get_db)
) -> ClientResponse:
    client = db.query(Client).filter(Client.id == id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    try:
        for attr, value in client_request.model_dump().items():
            setattr(client, attr, value)
        db.commit()
        db.refresh(client)
        return client

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Client with this email or CPF already exists.",
        )
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Database error while updating client."
        )


# Delete a client
@router.delete(
    "/{id}", status_code=204, dependencies=[Depends(get_current_admin_user)]
)
def delete_client(id: int, db: Session = Depends(get_db)) -> None:
    client = db.get(Client, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    try:
        db.delete(client)
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500, detail="Database error while deleting client."
        )
