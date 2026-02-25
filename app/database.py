from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

# Obtener configuración
settings = get_settings()

# Crear conexión a PostgreSQL
engine = create_engine(settings.DATABASE_URL)

# Crear fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()


def get_db():
    """
    Dependency: Abre una conexión a la BD y la cierra al terminar.
    Se usa en cada endpoint que necesite acceder a la BD.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()