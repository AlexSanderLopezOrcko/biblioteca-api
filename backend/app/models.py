from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    nacionalidad = Column(String, nullable=True)

    libros = relationship("Libro", back_populates="autor")


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False, unique=True)
    descripcion = Column(String, nullable=True)

    libros = relationship("Libro", back_populates="categoria")


class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    anio = Column(Integer, nullable=True)
    imagen_url = Column(String, nullable=True)
    autor_id = Column(Integer, ForeignKey("autores.id"), nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    autor = relationship("Autor", back_populates="libros")
    categoria = relationship("Categoria", back_populates="libros")
