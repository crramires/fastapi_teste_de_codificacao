from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.client_model import Client
from core.dependencies import get_db

router = APIRouter(prefix="/clients")


class ClientResponse(BaseModel):
    id: int
    name: str
    email: str
    cpf: str

    class Config:
        from_attributes = True


class ClientRequest(BaseModel):
    name: str
    email: str
    cpf: str


# List all clients
@router.get("", response_model=List[ClientResponse])
def get_client(db: Session = Depends(get_db)) -> List[ClientResponse]:
    return db.query(Client).all()


# List a client by id
@router.get("/{id}", response_model=ClientResponse)
def get_client_by_id(id: int, db: Session = Depends(get_db)) -> ClientResponse:
    client = db.get(Client, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


# Create a new client
@router.post("", response_model=ClientResponse, status_code=201)
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
@router.put("/{id}", response_model=ClientResponse, status_code=200)
def update_client(
    id: int, client_request: ClientRequest, db: Session = Depends(get_db)
) -> ClientResponse:
    client = db.get(Client, id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    try:
        client.name = client_request.name
        client.email = client_request.email
        client.cpf = client_request.cpf
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
            status_code=500, detail="Database error while updating client."
        )


# Delete a client
@router.delete("/{id}", status_code=204)
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
