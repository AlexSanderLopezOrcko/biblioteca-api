from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from app.database import Base, actualizar_tablas, engine
from app.routers import autores, categorias, libros
from app.seed import cargar_datos_iniciales

Base.metadata.create_all(bind=engine)
actualizar_tablas()
cargar_datos_iniciales()

app = FastAPI(title="Biblioteca API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def inicio():
    return RedirectResponse(url="/docs")


@app.get("/health", summary="Health")
def health():
    return {"status": "ok"}


app.include_router(libros.router)
app.include_router(autores.router)
app.include_router(categorias.router)
