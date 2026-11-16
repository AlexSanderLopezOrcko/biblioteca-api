from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/api/v1/categorias", tags=["categorias"])


def obtener_categoria(db: Session, categoria_id: int) -> models.Categoria:
    categoria = db.get(models.Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria


def validar_nombre_unico(db: Session, nombre: str, excluir_id: int | None = None):
    query = db.query(models.Categoria).filter(models.Categoria.nombre == nombre)
    if excluir_id is not None:
        query = query.filter(models.Categoria.id != excluir_id)
    if query.first():
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre")


@router.post("", response_model=schemas.CategoriaOut, status_code=201, summary="Crear categoría")
def crear_categoria(datos: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    validar_nombre_unico(db, datos.nombre)
    categoria = models.Categoria(**datos.model_dump())
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria


@router.get("", response_model=List[schemas.CategoriaOut], summary="Listar categorías")
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(models.Categoria).all()


@router.get("/{categoria_id}", response_model=schemas.CategoriaOut, summary="Obtener categoría")
def ver_categoria(categoria_id: int, db: Session = Depends(get_db)):
    return obtener_categoria(db, categoria_id)


@router.put("/{categoria_id}", response_model=schemas.CategoriaOut, summary="Actualizar categoría")
def actualizar_categoria(categoria_id: int, datos: schemas.CategoriaUpdate, db: Session = Depends(get_db)):
    categoria = obtener_categoria(db, categoria_id)
    cambios = datos.model_dump(exclude_unset=True)
    if "nombre" in cambios:
        validar_nombre_unico(db, cambios["nombre"], excluir_id=categoria_id)
    for campo, valor in cambios.items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria


@router.delete("/{categoria_id}", status_code=204, summary="Eliminar categoría")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = obtener_categoria(db, categoria_id)
    if categoria.libros:
        raise HTTPException(status_code=400, detail="La categoría tiene libros asociados")
    db.delete(categoria)
    db.commit()
