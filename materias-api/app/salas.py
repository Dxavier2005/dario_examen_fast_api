# app/materias.py — segunda parte: el CRUD


@router.get("", response_model=list[Materia])
def listar_materias(
    semestre: Annotated[int | None, Query(ge=1, le=10)] = None,
    solo_obligatorias: bool = False,
) -> list[dict]:
    resultado = MATERIAS
    if semestre is not None:
        resultado = [m for m in resultado if m["semestre"] == semestre]
    if solo_obligatorias:
        resultado = [m for m in resultado if m["obligatoria"]]
    return resultado


@router.post("", response_model=Materia, status_code=status.HTTP_201_CREATED)
def crear_materia(nueva: MateriaCrear) -> dict:
    if any(m["codigo"] == nueva.codigo for m in MATERIAS):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La materia '{nueva.codigo}' ya existe",
        )
    MATERIAS.append(nueva.model_dump())
    return MATERIAS[-1]


@router.get("/{codigo}", response_model=Materia)
def ver_materia(materia: MateriaEncontrada) -> dict:
    return materia


@router.put("/{codigo}", response_model=Materia)
def actualizar_materia(cambios: MateriaActualizar, materia: MateriaEncontrada) -> dict:
    materia.update(cambios.model_dump(exclude_unset=True))
    return materia


@router.delete("/{codigo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_materia(materia: MateriaEncontrada) -> None:
    MATERIAS.remove(materia)