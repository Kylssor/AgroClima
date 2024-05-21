from typing import Annotated
import uuid
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from Continair.container import Container
from Models.Roles.roles import Roles
from Models.User.user import User
from Schemas.Roles.roles_schema import Roles_schema
from Services.Roles.roles_service import Roles_service


roles_router = APIRouter(
    prefix="/Roles",
    tags=["Roles"],
)


container = Container()
auth_service = container.authentication_service()


@roles_router.get("/", response_model=list[Roles])
@inject
async def get_all(
    service: Roles_service = Depends(Provide[Container.roles_service])
):
    return service.get_all()


@roles_router.get("/{id}", response_model=Roles)
@inject
async def get_by_id(
    id: uuid.UUID,
    service: Roles_service = Depends(Provide[Container.roles_service])
):
    return service.get_by_id(id)


@roles_router.post("/", response_model=Roles)
@inject
async def create(
    data: Roles_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Roles_service = Depends(Provide[Container.roles_service])
):
    return service.create(data)


@roles_router.patch("/", response_model=Roles)
@inject
async def update(
    data: Roles_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Roles_service = Depends(Provide[Container.roles_service])
):
    return service.update(data)


@roles_router.delete("/{id}", status_code=204)
@inject
async def delete(
    id: uuid.UUID,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Roles_service = Depends(Provide[Container.roles_service])
):
    return service.delete(id)