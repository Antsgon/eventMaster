from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas

# Crear router con prefijo /recintos
router = APIRouter(
    prefix="/recintos",
    tags=["Recintos"]
)


# CREATE - Crear un recinto
@router.post("/", response_model=schemas.RecintoResponse, status_code=status.HTTP_201_CREATED)
def crear_recinto(recinto: schemas.RecintoCreate, db: Session = Depends(get_db)):
    db_recinto = models.Recinto(**recinto.model_dump())
    db.add(db_recinto)
    db.commit()
    db.refresh(db_recinto)
    return db_recinto


# READ ALL - Obtener todos los recintos
@router.get("/", response_model=List[schemas.RecintoResponse])
def obtener_recintos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    recintos = db.query(models.Recinto).offset(skip).limit(limit).all()
    return recintos


# READ ONE - Obtener un recinto por ID
@router.get("/{recinto_id}", response_model=schemas.RecintoResponse)
def obtener_recinto(recinto_id: int, db: Session = Depends(get_db)):
    recinto = db.query(models.Recinto).filter(models.Recinto.id == recinto_id).first()
    if not recinto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recinto con id {recinto_id} no encontrado"
        )
    return recinto


# UPDATE - Actualizar un recinto
@router.put("/{recinto_id}", response_model=schemas.RecintoResponse)
def actualizar_recinto(recinto_id: int, recinto: schemas.RecintoUpdate, db: Session = Depends(get_db)):
    db_recinto = db.query(models.Recinto).filter(models.Recinto.id == recinto_id).first()
    if not db_recinto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recinto con id {recinto_id} no encontrado"
        )

    update_data = recinto.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_recinto, key, value)

    db.commit()
    db.refresh(db_recinto)
    return db_recinto


# DELETE - Eliminar un recinto
@router.delete("/{recinto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_recinto(recinto_id: int, db: Session = Depends(get_db)):
    db_recinto = db.query(models.Recinto).filter(models.Recinto.id == recinto_id).first()
    if not db_recinto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Recinto con id {recinto_id} no encontrado"
        )

    db.delete(db_recinto)
    db.commit()
    return None