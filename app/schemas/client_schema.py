from pydantic import BaseModel


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
