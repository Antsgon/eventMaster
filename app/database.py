from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import get_settings

settings = get_settings()
print(">>> DATABASE_URL EN PRODUCCIÓN:", repr(settings.DATABASE_URL))
DATABASE_URL = settings.DATABASE_URL

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

print(">>> DATABASE_URL EN PRODUCCIÓN:", repr(settings.DATABASE_URL))
engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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