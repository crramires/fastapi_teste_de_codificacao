import uvicorn
from fastapi import FastAPI

from app.api.v1.controllers import (
    clients_controller,
    order_and_orderProduct_controller,
    products_controller,
)

app = FastAPI()


@app.get("/")
def root() -> str:
    return "Servidor rodando..."


app.include_router(clients_controller.router)
app.include_router(products_controller.router)
app.include_router(order_and_orderProduct_controller.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
