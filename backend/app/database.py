from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = Path(__file__).resolve().parent.parent / "biblioteca.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def actualizar_tablas():
    columnas = [c["name"] for c in inspect(engine).get_columns("libros")]
    if "imagen_url" not in columnas:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE libros ADD COLUMN imagen_url VARCHAR"))
