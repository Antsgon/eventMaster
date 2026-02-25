from pydantic import BaseModel, Field, field_validator
from datetime import date
from typing import Optional, List


# RECINTO

class RecintoBase(BaseModel):
    """Campos comunes de Recinto"""
    nombre: str
    ciudad: str
    capacidad: int = Field(gt=0, description="Debe ser mayor a 0")


class RecintoCreate(RecintoBase):
    """Para crear un recinto (POST)"""
    pass


class RecintoUpdate(BaseModel):
    """Para actualizar un recinto (PUT) - todos opcionales"""
    nombre: Optional[str] = None
    ciudad: Optional[str] = None
    capacidad: Optional[int] = Field(default=None, gt=0)


class RecintoResponse(RecintoBase):
    """Lo que devuelve la API"""
    id: int

    class Config:
        from_attributes = True  # Permite convertir desde SQLAlchemy


#  EVENTO

class EventoBase(BaseModel):
    """Campos comunes de Evento"""
    nombre: str
    fecha: date
    precio: float = Field(ge=0, description="No puede ser negativo")
    recinto_id: int


class EventoCreate(EventoBase):
    """Para crear un evento (POST)"""

    @field_validator('precio')
    @classmethod
    def precio_no_negativo(cls, v):
        if v < 0:
            raise ValueError('El precio no puede ser negativo')
        return v


class EventoUpdate(BaseModel):
    """Para actualizar un evento (PUT) - todos opcionales"""
    nombre: Optional[str] = None
    fecha: Optional[date] = None
    precio: Optional[float] = Field(default=None, ge=0)


class EventoResponse(EventoBase):
    """Lo que devuelve la API"""
    id: int
    tickets_vendidos: int

    class Config:
        from_attributes = True


class EventoConRecinto(EventoResponse):
    """Evento con datos del recinto incluidos"""
    recinto: RecintoResponse


# COMPRA

class CompraTickets(BaseModel):
    """Para comprar tickets (PATCH)"""
    cantidad: int = Field(gt=0, description="Debe ser mayor a 0")