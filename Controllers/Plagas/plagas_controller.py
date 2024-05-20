from typing import Annotated
import uuid
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from Continair.container import Container
from Models.Plagas.plagas import Plags
from Models.User.user import User
from Schemas.Plagas.plagas_schema import Plagas_schema
from Services.Plagas.plagas_service import Plagas_service


plagas_router = APIRouter(
    prefix="/Plagas",
    tags=["Plagas"],
)


container = Container()
auth_service = container.authentication_service()


@plagas_router.get("/", response_model=list[Plags])
@inject
async def get_all(
    service: Plagas_service = Depends(Provide[Container.plagas_service])
):
    return service.get_all()


@plagas_router.get("/{id}", response_model=Plags)
@inject
async def get_by_id(
    id: uuid.UUID,
    service: Plagas_service = Depends(Provide[Container.plantas_service])
):
    return service.get_by_id(id)


@plagas_router.post("/", response_model=Plags)
@inject
async def create(
    data: Plagas_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Plagas_service = Depends(Provide[Container.plagas_service])
):
    return service.create(data)


@plagas_router.patch("/", response_model=Plags)
@inject
async def update(
    data: Plagas_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Plagas_service = Depends(Provide[Container.plagas_service])
):
    return service.update(data)


@plagas_router.delete("/{id}", status_code=204)
@inject
async def delete(
    id: uuid.UUID,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Plagas_service = Depends(Provide[Container.plagas_service])
):
    return service.delete(id)