from typing import Annotated
from fastapi import APIRouter, Depends, Query
from dependency_injector.wiring import Provide, inject

from Continair.container import Container
from Models.RecordatoriosCuidados.recordCui import RecordCui
from Models.User.user import User
from Services.RecordatoriosCuidados.recordatorio_cuidado_service import RecordatorioCuidado_service


alertas_router = APIRouter(
    prefix="/Alertas",
    tags=["Alertas"],
)


container = Container()
auth_service = container.authentication_service()


@alertas_router.get("/", response_model=list[RecordCui])
@inject
async def get_alertas(
    user: Annotated[User, Depends(auth_service.check_session)],
    dias_proximos: int = Query(default=3, ge=0),
    service: RecordatorioCuidado_service = Depends(Provide[Container.recordatorios_cuidados_service])
):
    return service.get_alertas(user.id, dias_proximos)
