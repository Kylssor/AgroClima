from typing import Annotated
import uuid
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject

from Continair.container import Container
from Models.RecordatoriosCuidados.recordCui import RecordCui
from Models.User.user import User
from Schemas.RecordatoriosCuidados.recordatorio_cuidado_schema import RecordatorioCuidado_schema
from Services.RecordatoriosCuidados.recordatorio_cuidado_service import RecordatorioCuidado_service


recordatorios_cuidados_router = APIRouter(
    prefix="/RecordatoriosCuidados",
    tags=["RecordatoriosCuidados"],
)


container = Container()
auth_service = container.authentication_service()


@recordatorios_cuidados_router.get("/", response_model=list[RecordCui])
@inject
async def get_by_plantacion(
    plantacion_id: uuid.UUID,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: RecordatorioCuidado_service = Depends(Provide[Container.recordatorios_cuidados_service])
):
    return service.get_by_plantacion(plantacion_id, user.id)


@recordatorios_cuidados_router.post("/", response_model=RecordCui)
@inject
async def create(
    data: RecordatorioCuidado_schema,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: RecordatorioCuidado_service = Depends(Provide[Container.recordatorios_cuidados_service])
):
    return service.create(data, user.id)


@recordatorios_cuidados_router.patch("/{id}/cumplido", response_model=RecordCui)
@inject
async def marcar_cumplido(
    id: uuid.UUID,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: RecordatorioCuidado_service = Depends(Provide[Container.recordatorios_cuidados_service])
):
    return service.marcar_cumplido(id, user.id)


@recordatorios_cuidados_router.delete("/{id}", status_code=204)
@inject
async def delete(
    id: uuid.UUID,
    user: Annotated[User, Depends(auth_service.check_session)],
    service: RecordatorioCuidado_service = Depends(Provide[Container.recordatorios_cuidados_service])
):
    return service.delete(id, user.id)
