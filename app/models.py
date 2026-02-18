from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Recinto(Base):
    """
    Tabla: recintos
    Representa un lugar donde se hacen eventos (estadio, teatro, etc.)
    """
    __tablename__ = "recintos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    ciudad = Column(String(100), nullable=False)
    capacidad = Column(Integer, nullable=False)

    # Relación: Un recinto tiene muchos eventos
    eventos = relationship("Evento", back_populates="recinto", cascade="all, delete-orphan")


class Evento(Base):
    """
    Tabla: eventos
    Representa un evento (concierto, obra de teatro, etc.)
    """
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    fecha = Column(Date, nullable=False)
    precio = Column(Float, nullable=False)
    tickets_vendidos = Column(Integer, default=0)
    recinto_id = Column(Integer, ForeignKey("recintos.id"), nullable=False)

    # Relación: Un evento pertenece a un recinto
    recinto = relationship("Recinto", back_populates="eventos")