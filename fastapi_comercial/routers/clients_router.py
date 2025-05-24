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
        orm_mode = True


class ClientRequest(BaseModel):
    name: str
    email: str
    cpf: str


@router.get("", response_model=List[ClientResponse])
def get_client(db: Session = Depends(get_db)) -> List[ClientResponse]:
    return db.query(Client).all()


@router.post("", response_model=ClientResponse, status_code=201)
def create_client(
    client_request: ClientRequest, db: Session = Depends(get_db)
) -> ClientResponse:
    client = Client(**client_request.model_dump())

    db.add(client)
    db.commit()
    db.refresh(client)

    return client
