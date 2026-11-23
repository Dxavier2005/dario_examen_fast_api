from fastapi import FastAPI

from app.salas import router as salas_router

app = FastAPI(title="API Cine - Salas", version="1.0.0")
app.include_router(salas_router)