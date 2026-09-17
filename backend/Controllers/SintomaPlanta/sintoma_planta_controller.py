from typing import Annotated, Optional
import uuid
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from Continair.container import Container
from Models.SintomaPlanta.sintoma_planta import Sintoma_Planta
from Models.User.user import User
from Schemas.SintomaPlanta.sintoma_planta_schema import SintomaPlanta_schema
from Services.SintomaPlanta.sintoma_planta_service import SintomaPlanta_service


sintoma_planta_router = APIRouter(
    prefix="/SintomasPlanta",
    tags=["SintomasPlanta"],
)


container = Container()
auth_service = container.authentication_service()


@sintoma_planta_router.get("/", response_model=list[Sintoma_Planta])
@inject
async def get_all(
    planta_id: Optional[uuid.UUID] = None,
    service: SintomaPlanta_service = Depends(Provide[Container.sintoma_planta_service])
):
    if planta_id:
        return service.get_by_planta(planta_id)
    return service.get_all()


@sintoma_planta_router.get("/{id}", response_model=Sintoma_Planta)
@inject
async def get_by_id(
    id: uuid.UUID,
    service: SintomaPlanta_service = Depends(Provide[Container.sintoma_planta_service])
):
    return service.get_by_id(id)


@sintoma_planta_router.post("/", response_model=Sintoma_Planta)
@inject
async def create(
    data: SintomaPlanta_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: SintomaPlanta_service = Depends(Provide[Container.sintoma_planta_service])
):
    return service.create(data)


@sintoma_planta_router.patch("/", response_model=Sintoma_Planta)
@inject
async def update(
    data: SintomaPlanta_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: SintomaPlanta_service = Depends(Provide[Container.sintoma_planta_service])
):
    return service.update(data)


@sintoma_planta_router.delete("/{id}", status_code=204)
@inject
async def delete(
    id: uuid.UUID,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: SintomaPlanta_service = Depends(Provide[Container.sintoma_planta_service])
):
    return service.delete(id)
