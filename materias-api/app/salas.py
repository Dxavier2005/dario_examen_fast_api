from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.datos import SALAS
from app.esquemas import SalaActualizar, SalaCrear, SalaSalida

router = APIRouter(prefix="/salas", tags=["Salas"])


def buscar_sala(codigo: str) -> dict:
    codigo_normalizado = codigo.upper()
    for sala in SALAS:
        if sala["codigo"] == codigo_normalizado:
            return sala
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No existe la sala '{codigo_normalizado}'",
    )


SalaDependencia = Annotated[dict, Depends(buscar_sala)]


# Rutas literales primero (antes de /{codigo})
@router.get("/aforo-jornada")
def aforo_jornada(
    funciones: Annotated[int, Query(ge=1, le=12)],
    piso: Annotated[int | None, Query(ge=1, le=5)] = None,
) -> dict:
    seleccion = [s for s in SALAS if piso is None or s["piso"] == piso]
    if not seleccion:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay salas para el criterio indicado",
        )

    total_salas = len(seleccion)
    suma_butacas = 0
    suma_vendible_por_sala = 0
    salas_3d = 0

    for sala in seleccion:
        butacas = sala["butacas"]
        suma_butacas += butacas
        suma_vendible_por_sala += int(butacas * 0.90)
        if sala["es_3d"]:
            salas_3d += 1

    return {
        "salas": total_salas,
        "funciones": funciones,
        "butacas_promedio": round(suma_butacas / total_salas, 2),
        "aforo_total": suma_butacas * funciones,
        "aforo_vendible": suma_vendible_por_sala * funciones,
        "porcentaje_3d": round((salas_3d * 100) / total_salas, 1),
    }


@router.get("/mantenimiento-salas")
def mantenimiento_salas(
    en_mantenimiento: Annotated[list[str] | None, Query()] = None,
) -> dict:
    if not SALAS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay salas registradas",
        )

    codigos_fuera = {c.upper() for c in en_mantenimiento} if en_mantenimiento else set()

    total = 0
    fuera_servicio = 0
    operativas = 0
    aforo_operativo = 0
    mayor_butacas = -1
    sala_operativa_mayor: str | None = None

    for sala in SALAS:
        total += 1
        if sala["codigo"] in codigos_fuera:
            fuera_servicio += 1
        else:
            operativas += 1
            butacas = sala["butacas"]
            aforo_operativo += butacas
            if butacas > mayor_butacas:
                mayor_butacas = butacas
                sala_operativa_mayor = sala["codigo"]

    return {
        "total": total,
        "en_mantenimiento": fuera_servicio,
        "operativas": operativas,
        "porcentaje_fuera_de_servicio": round((fuera_servicio * 100) / total, 1),
        "aforo_operativo": aforo_operativo,
        "sala_operativa_mayor": sala_operativa_mayor,
    }


# CRUD del recurso
@router.get("", response_model=list[SalaSalida], status_code=status.HTTP_200_OK)
def listar_salas(
    piso: Annotated[int | None, Query(ge=1, le=5)] = None,
    es_3d: bool | None = None,
) -> list[dict]:
    resultado = SALAS
    if piso is not None:
        resultado = [s for s in resultado if s["piso"] == piso]
    if es_3d is not None:
        resultado = [s for s in resultado if s["es_3d"] == es_3d]
    return resultado


@router.post("", response_model=SalaSalida, status_code=status.HTTP_201_CREATED)
def crear_sala(sala: SalaCrear) -> dict:
    if any(s["codigo"] == sala.codigo for s in SALAS):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La sala '{sala.codigo}' ya existe",
        )
    nueva = sala.model_dump()
    SALAS.append(nueva)
    return nueva


@router.get("/{codigo}", response_model=SalaSalida, status_code=status.HTTP_200_OK)
def ver_sala(sala: SalaDependencia) -> dict:
    return sala


@router.patch("/{codigo}", response_model=SalaSalida, status_code=status.HTTP_200_OK)
def actualizar_sala(cambios: SalaActualizar, sala: SalaDependencia) -> dict:
    sala.update(cambios.model_dump(exclude_unset=True))
    return sala


@router.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_sala(sala: SalaDependencia) -> Response:
    SALAS.remove(sala)
    return Response(status_code=status.HTTP_204_NO_CONTENT)