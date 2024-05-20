from typing import Annotated
import uuid
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from Continair.container import Container
from Models.Plantas.plantas_Cat import  Plantas_Cat  
from Models.User.user import User
from Schemas.Plantas.plantasCat_schema import PlantasCat_schema
from Services.Plantas.plantasCat_service import PlantasCat_service


plantasCat_router = APIRouter(
    prefix="/plantascategory",
    tags=["Plantas Category"],
)


container = Container()
auth_service = container.authentication_service()


@plantasCat_router.get("/", response_model=list[Plantas_Cat])
@inject
async def get_all(
    service: PlantasCat_service = Depends(Provide[Container.plantas_cat_service])
):
    return service.get_all()


@plantasCat_router.get("/{id}", response_model=Plantas_Cat)
@inject
async def get_by_id(
    id: uuid.UUID,
    service: PlantasCat_service = Depends(Provide[Container.plantas_cat_service])
):
    return service.get_by_id(id)


@plantasCat_router.post("/", response_model=Plantas_Cat)
@inject
async def create(
    data: PlantasCat_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: PlantasCat_service = Depends(Provide[Container.plantas_cat_service])
):
    return service.create(data)


@plantasCat_router.patch("/", response_model=Plantas_Cat)
@inject
async def update(
    data: PlantasCat_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: PlantasCat_service = Depends(Provide[Container.plantas_cat_service])
):
    return service.update(data)


@plantasCat_router.delete("/{id}", status_code=204)
@inject
async def delete(
    id: uuid.UUID,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: PlantasCat_service = Depends(Provide[Container.plantas_cat_service])
):
    return service.delete(id)