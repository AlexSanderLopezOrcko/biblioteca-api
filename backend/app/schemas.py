from typing import Optional

from pydantic import BaseModel, ConfigDict


class AutorBase(BaseModel):
    nombre: str
    nacionalidad: Optional[str] = None


class AutorCreate(AutorBase):
    pass


class AutorUpdate(BaseModel):
    nombre: Optional[str] = None
    nacionalidad: Optional[str] = None


class AutorOut(AutorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


class CategoriaOut(CategoriaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class LibroBase(BaseModel):
    titulo: str
    anio: Optional[int] = None
    autor_id: int
    categoria_id: int


class LibroCreate(LibroBase):
    pass


class LibroUpdate(BaseModel):
    titulo: Optional[str] = None
    anio: Optional[int] = None
    autor_id: Optional[int] = None
    categoria_id: Optional[int] = None


class LibroOut(LibroBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    autor: AutorOut
    categoria: CategoriaOut
