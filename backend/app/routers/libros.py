from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/v1/libros", tags=["libros"])


def obtener_libro(db: Session, libro_id: int) -> models.Libro:
    libro = db.get(models.Libro, libro_id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro


def validar_relaciones(db: Session, autor_id: Optional[int], categoria_id: Optional[int]):
    if autor_id is not None and not db.get(models.Autor, autor_id):
        raise HTTPException(status_code=400, detail="El autor no existe")
    if categoria_id is not None and not db.get(models.Categoria, categoria_id):
        raise HTTPException(status_code=400, detail="La categoría no existe")


@router.post("", response_model=schemas.LibroOut, status_code=201, summary="Crear libro")
def crear_libro(datos: schemas.LibroCreate, db: Session = Depends(get_db)):
    validar_relaciones(db, datos.autor_id, datos.categoria_id)
    libro = models.Libro(**datos.model_dump())
    db.add(libro)
    db.commit()
    db.refresh(libro)
    return libro


@router.get("", response_model=List[schemas.LibroOut], summary="Listar libros")
def listar_libros(
    buscar: Optional[str] = Query(None, description="Buscar por título o autor"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Libro).join(models.Autor)
    if buscar:
        patron = f"%{buscar}%"
        query = query.filter(models.Libro.titulo.ilike(patron) | models.Autor.nombre.ilike(patron))
    if categoria_id is not None:
        query = query.filter(models.Libro.categoria_id == categoria_id)
    return query.all()


@router.get("/{libro_id}", response_model=schemas.LibroOut, summary="Obtener libro")
def ver_libro(libro_id: int, db: Session = Depends(get_db)):
    return obtener_libro(db, libro_id)


@router.put("/{libro_id}", response_model=schemas.LibroOut, summary="Actualizar libro")
def actualizar_libro(libro_id: int, datos: schemas.LibroUpdate, db: Session = Depends(get_db)):
    libro = obtener_libro(db, libro_id)
    cambios = datos.model_dump(exclude_unset=True)
    validar_relaciones(db, cambios.get("autor_id"), cambios.get("categoria_id"))
    for campo, valor in cambios.items():
        setattr(libro, campo, valor)
    db.commit()
    db.refresh(libro)
    return libro


@router.delete("/{libro_id}", status_code=204, summary="Eliminar libro")
def eliminar_libro(libro_id: int, db: Session = Depends(get_db)):
    libro = obtener_libro(db, libro_id)
    db.delete(libro)
    db.commit()
