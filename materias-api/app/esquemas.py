from pydantic import BaseModel, Field


class SalaCrear(BaseModel):
    codigo: str = Field(..., pattern=r"^[A-Z]{3}\d{3}$")
    nombre: str = Field(..., min_length=3, max_length=60)
    butacas: int = Field(..., ge=20, le=500)
    piso: int = Field(..., ge=1, le=5)
    es_3d: bool = False


class SalaActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=3, max_length=60)
    butacas: int | None = Field(default=None, ge=20, le=500)
    piso: int | None = Field(default=None, ge=1, le=5)
    es_3d: bool | None = None


class SalaSalida(BaseModel):
    codigo: str
    nombre: str
    butacas: int
    piso: int
    es_3d: bool