from fastapi import FastAPI
from .database import engine, Base
from .routers import recintos, eventos

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="EventMaster API",
    description="API para gestión de recintos y venta de entradas",
    version="1.0.0"
)

# Incluir routers
app.include_router(recintos.router)
app.include_router(eventos.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bienvenido a EventMaster API",
        "docs": "/docs"
    }