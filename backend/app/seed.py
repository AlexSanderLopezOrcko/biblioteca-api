from app import models
from app.database import SessionLocal

AUTORES = [
    ("Gabriel García Márquez", "Colombiana"),
    ("Miguel de Cervantes", "Española"),
    ("Stephen Hawking", "Británica"),
    ("Yuval Noah Harari", "Israelí"),
    ("Charles Darwin", "Británica"),
    ("Antoine de Saint-Exupéry", "Francesa"),
]

CATEGORIAS = [
    ("Novela", "Obras de ficción narrativa"),
    ("Ciencia", "Divulgación científica"),
    ("Historia", "Libros sobre historia de la humanidad"),
    ("Otro", "Otros géneros"),
]

LIBROS = [
    ("Cien años de soledad", 1967, "Gabriel García Márquez", "Novela"),
    ("Don Quijote de la Mancha", 1605, "Miguel de Cervantes", "Novela"),
    ("Breve historia del tiempo", 1988, "Stephen Hawking", "Ciencia"),
    ("Sapiens", 2011, "Yuval Noah Harari", "Historia"),
    ("El origen de las especies", 1859, "Charles Darwin", "Ciencia"),
    ("El principito", 1943, "Antoine de Saint-Exupéry", "Otro"),
]


def cargar_datos_iniciales():
    db = SessionLocal()
    try:
        if db.query(models.Libro).first() or db.query(models.Autor).first():
            return

        autores = {nombre: models.Autor(nombre=nombre, nacionalidad=nac) for nombre, nac in AUTORES}
        categorias = {nombre: models.Categoria(nombre=nombre, descripcion=desc) for nombre, desc in CATEGORIAS}
        db.add_all(list(autores.values()) + list(categorias.values()))

        for titulo, anio, autor, categoria in LIBROS:
            db.add(models.Libro(titulo=titulo, anio=anio, autor=autores[autor], categoria=categorias[categoria]))

        db.commit()
    finally:
        db.close()
