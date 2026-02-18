from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas

# Crear router con prefijo /eventos
router = APIRouter(
    prefix="/eventos",
    tags=["Eventos"]
)


# CREATE - Crear un evento
@router.post("/", response_model=schemas.EventoResponse, status_code=status.HTTP_201_CREATED)
def crear_evento(evento: schemas.EventoCreate, db: Session = Depends(get_db)):
    # Verificar que el recinto existe
    recinto = db.query(models.Recinto).filter(models.Recinto.id == evento.recinto_id).first()
    if not recinto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recinto con id {evento.recinto_id} no encontrado"
        )

    db_evento = models.Evento(**evento.model_dump())
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento


# READ ALL - Obtener todos los eventos (con filtro opcional por ciudad)
@router.get("/", response_model=List[schemas.EventoConRecinto])
def obtener_eventos(
        ciudad: Optional[str] = Query(None, description="Filtrar por ciudad del recinto"),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    query = db.query(models.Evento).join(models.Recinto)

    if ciudad:
        query = query.filter(models.Recinto.ciudad.ilike(f"%{ciudad}%"))

    eventos = query.offset(skip).limit(limit).all()
    return eventos


# READ ONE - Obtener un evento por ID
@router.get("/{evento_id}", response_model=schemas.EventoConRecinto)
def obtener_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(models.Evento).filter(models.Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evento con id {evento_id} no encontrado"
        )
    return evento


# UPDATE - Actualizar un evento
@router.put("/{evento_id}", response_model=schemas.EventoResponse)
def actualizar_evento(evento_id: int, evento: schemas.EventoUpdate, db: Session = Depends(get_db)):
    db_evento = db.query(models.Evento).filter(models.Evento.id == evento_id).first()
    if not db_evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evento con id {evento_id} no encontrado"
        )

    update_data = evento.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_evento, key, value)

    db.commit()
    db.refresh(db_evento)
    return db_evento


# DELETE - Eliminar un evento
@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_evento(evento_id: int, db: Session = Depends(get_db)):
    db_evento = db.query(models.Evento).filter(models.Evento.id == evento_id).first()
    if not db_evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evento con id {evento_id} no encontrado"
        )

    db.delete(db_evento)
    db.commit()
    return None


# COMPRAR TICKETS - Lógica de negocio principal
@router.patch("/{evento_id}/comprar", response_model=schemas.EventoResponse)
def comprar_tickets(evento_id: int, compra: schemas.CompraTickets, db: Session = Depends(get_db)):
    # Obtener evento
    evento = db.query(models.Evento).filter(models.Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Evento con id {evento_id} no encontrado"
        )

    # Verificar aforo
    capacidad_recinto = evento.recinto.capacidad
    tickets_actuales = evento.tickets_vendidos
    tickets_solicitados = compra.cantidad

    if tickets_actuales + tickets_solicitados > capacidad_recinto:
        disponibles = capacidad_recinto - tickets_actuales
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No hay aforo suficiente. Disponibles: {disponibles}, Solicitados: {tickets_solicitados}"
        )

    # Actualizar tickets vendidos
    evento.tickets_vendidos += tickets_solicitados
    db.commit()
    db.refresh(evento)
    return evento