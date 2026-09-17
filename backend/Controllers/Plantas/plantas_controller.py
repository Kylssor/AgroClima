from typing import Annotated
import uuid
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from Continair.container import Container
from Models.Plantas.plantas import Plantas
from Models.User.user import User
from Schemas.Plantas.plantas_schema import Plantas_schema
from Services.Plantas.plantas_service import Plantas_service


plantas_router = APIRouter(
    prefix="/Plantas",
    tags=["Plantas"],
)


container = Container()
auth_service = container.authentication_service()


@plantas_router.get("/", response_model=list[Plantas])
@inject
async def get_all(
    service: Plantas_service = Depends(Provide[Container.plantas_service])
):
    return service.get_all()


@plantas_router.get("/{id}", response_model=Plantas)
@inject
async def get_by_id(
    id: uuid.UUID,
    service: Plantas_service = Depends(Provide[Container.plantas_service])
):
    return service.get_by_id(id)


@plantas_router.post("/", response_model=Plantas)
@inject
async def create(
    data: Plantas_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Plantas_service = Depends(Provide[Container.plantas_service])
):
    return service.create(data)


@plantas_router.patch("/", response_model=Plantas)
@inject
async def update(
    data: Plantas_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Plantas_service = Depends(Provide[Container.plantas_service])
):
    return service.update(data)


@plantas_router.delete("/{id}", status_code=204)
@inject
async def delete(
    id: uuid.UUID,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Plantas_service = Depends(Provide[Container.plantas_service])
):
    return service.delete(id)