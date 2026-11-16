from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/v1/autores", tags=["autores"])


def obtener_autor(db: Session, autor_id: int) -> models.Autor:
    autor = db.get(models.Autor, autor_id)
    if not autor:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor


@router.post("", response_model=schemas.AutorOut, status_code=201, summary="Crear autor")
def crear_autor(datos: schemas.AutorCreate, db: Session = Depends(get_db)):
    autor = models.Autor(**datos.model_dump())
    db.add(autor)
    db.commit()
    db.refresh(autor)
    return autor


@router.get("", response_model=List[schemas.AutorOut], summary="Listar autores")
def listar_autores(db: Session = Depends(get_db)):
    return db.query(models.Autor).all()


@router.get("/{autor_id}", response_model=schemas.AutorOut, summary="Obtener autor")
def ver_autor(autor_id: int, db: Session = Depends(get_db)):
    return obtener_autor(db, autor_id)


@router.put("/{autor_id}", response_model=schemas.AutorOut, summary="Actualizar autor")
def actualizar_autor(autor_id: int, datos: schemas.AutorUpdate, db: Session = Depends(get_db)):
    autor = obtener_autor(db, autor_id)
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(autor, campo, valor)
    db.commit()
    db.refresh(autor)
    return autor


@router.delete("/{autor_id}", status_code=204, summary="Eliminar autor")
def eliminar_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = obtener_autor(db, autor_id)
    if autor.libros:
        raise HTTPException(status_code=400, detail="El autor tiene libros asociados")
    db.delete(autor)
    db.commit()
