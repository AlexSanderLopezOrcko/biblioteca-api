from app import models
from app.database import SessionLocal

PORTADA = "https://covers.openlibrary.org/b/isbn/{}-L.jpg"

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
    ("Cien años de soledad", 1967, "Gabriel García Márquez", "Novela", PORTADA.format("9780307474728")),
    ("Don Quijote de la Mancha", 1605, "Miguel de Cervantes", "Novela", PORTADA.format("9780060934347")),
    ("Breve historia del tiempo", 1988, "Stephen Hawking", "Ciencia", PORTADA.format("9780553380163")),
    ("Sapiens", 2011, "Yuval Noah Harari", "Historia", PORTADA.format("9780062316097")),
    ("El origen de las especies", 1859, "Charles Darwin", "Ciencia", PORTADA.format("9780451529060")),
    ("El principito", 1943, "Antoine de Saint-Exupéry", "Otro", PORTADA.format("9780156012195")),
]


def completar_portadas(db):
    portadas = {titulo: imagen for titulo, _, _, _, imagen in LIBROS}
    sin_imagen = db.query(models.Libro).filter(models.Libro.imagen_url.is_(None)).all()
    for libro in sin_imagen:
        if libro.titulo in portadas:
            libro.imagen_url = portadas[libro.titulo]
    db.commit()


def cargar_datos_iniciales():
    db = SessionLocal()
    try:
        if db.query(models.Libro).first() or db.query(models.Autor).first():
            completar_portadas(db)
            return

        autores = {nombre: models.Autor(nombre=nombre, nacionalidad=nac) for nombre, nac in AUTORES}
        categorias = {nombre: models.Categoria(nombre=nombre, descripcion=desc) for nombre, desc in CATEGORIAS}
        db.add_all(list(autores.values()) + list(categorias.values()))

        for titulo, anio, autor, categoria, imagen in LIBROS:
            db.add(
                models.Libro(
                    titulo=titulo,
                    anio=anio,
                    imagen_url=imagen,
                    autor=autores[autor],
                    categoria=categorias[categoria],
                )
            )

        db.commit()
    finally:
        db.close()
