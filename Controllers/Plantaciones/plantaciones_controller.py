from typing import Annotated
import uuid
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from Continair.container import Container
from Models.Plantaciones.plantaciones import Plants_mp
from Models.User.user import User
from Schemas.Plantaciones.plantaciones_schema import Plantaciones_schema
from Services.Plantaciones.plantaciones_service import Plantaciones_service


plantaciones_router = APIRouter(
    prefix="/Plantaciones",
    tags=["Plantaciones"],
)


container = Container()
auth_service = container.authentication_service()


@plantaciones_router.get("/", response_model=list[Plants_mp])
@inject
async def get_all(
    service: Plantaciones_service = Depends(Provide[Container.plantaciones_service])
):
    return service.get_all()


@plantaciones_router.get("/{id}", response_model=Plants_mp)
@inject
async def get_by_id(
    id: uuid.UUID,
    service: Plantaciones_service = Depends(Provide[Container.plantaciones_service])
):
    return service.get_by_id(id)


@plantaciones_router.post("/", response_model=Plants_mp)
@inject
async def create(
    data: Plantaciones_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Plantaciones_service = Depends(Provide[Container.plantaciones_service])
):
    return service.create(data)


@plantaciones_router.patch("/", response_model=Plants_mp)
@inject
async def update(
    data: Plantaciones_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Plantaciones_service = Depends(Provide[Container.plantaciones_service])
):
    return service.update(data)


@plantaciones_router.delete("/{id}", status_code=204)
@inject
async def delete(
    id: uuid.UUID,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Plantaciones_service = Depends(Provide[Container.plantaciones_service])
):
    return service.delete(id)