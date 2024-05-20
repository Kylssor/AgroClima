from typing import Annotated
import uuid
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from Continair.container import Container
from Models.PlagXPlants.plagxplants import Plagsxplants
from Models.User.user import User
from Schemas.PlagxPlants.plagxplants_schema import PlagxPlants_schema
from Services.PlagxPlants.plagxplants_service import Plagxplants_service


plagsxplants_router = APIRouter(
    prefix="/Plagsxplants",
    tags=["Plagsxplants"],
)


container = Container()
auth_service = container.authentication_service()


@plagsxplants_router.get("/", response_model=list[Plagsxplants])
@inject
async def get_all(
    service: Plagxplants_service = Depends(Provide[Container.plagas_service])
):
    return service.get_all()


@plagsxplants_router.get("/{id}", response_model=Plagsxplants)
@inject
async def get_by_id(
    id: uuid.UUID,
    service: Plagxplants_service = Depends(Provide[Container.plantas_service])
):
    return service.get_by_id(id)


@plagsxplants_router.post("/", response_model=Plagsxplants)
@inject
async def create(
    data: PlagxPlants_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Plagxplants_service = Depends(Provide[Container.plagas_service])
):
    return service.create(data)


@plagsxplants_router.patch("/", response_model=Plagsxplants)
@inject
async def update(
    data: PlagxPlants_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Plagxplants_service = Depends(Provide[Container.plagas_service])
):
    return service.update(data)


@plagsxplants_router.delete("/{id}", status_code=204)
@inject
async def delete(
    id: uuid.UUID,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: Plagxplants_service = Depends(Provide[Container.plagas_service])
):
    return service.delete(id)