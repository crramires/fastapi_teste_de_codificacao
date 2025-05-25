import uvicorn
from fastapi import FastAPI

from fastapi_comercial.routers import clients_router

app = FastAPI()


@app.get("/")
def root() -> str:
    return "Servidor rodando..."


app.include_router(clients_router.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
