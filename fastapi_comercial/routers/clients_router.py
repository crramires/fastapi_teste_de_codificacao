from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from fastapi_comercial.models.client_model import Client
from shared.dependencies import get_db

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


@router.get("", response_model=List[ClientResponse])
def get_client(db: Session = Depends(get_db)) -> List[ClientResponse]:
    return db.query(Client).all()


@router.get("/{id}", response_model=ClientResponse)
def get_client_by_id(id: int, db: Session = Depends(get_db)) -> ClientResponse:
    client: Client = db.query(Client).filter_by(id=id).first()
    return client


@router.post("", response_model=ClientResponse, status_code=201)
def create_client(
    client_request: ClientRequest, db: Session = Depends(get_db)
) -> ClientResponse:
    client = Client(**client_request.model_dump())

    db.add(client)
    db.commit()
    db.refresh(client)

    return client


@router.put("/{id}", response_model=ClientResponse, status_code=200)
def update_client(
    id: int, client_request: ClientRequest, db: Session = Depends(get_db)
) -> ClientResponse:
    client = db.query(Client).get(id)
    client.name = client_request.name
    client.email = client_request.email
    client.cpf = client_request.cpf

    db.add(client)
    db.commit()
    db.refresh(client)
    return client


@router.delete("/{id}", status_code=204)
def delete_client(id: int, db: Session = Depends(get_db)) -> None:
    client = db.query(Client).filter_by(id)
    db.delete(client)
    db.commit()
