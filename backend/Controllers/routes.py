from fastapi import APIRouter

from Controllers.Auth.auth_controller import auth_router
from Controllers.Plantas.plantas_controller import plantas_router
from Controllers.Plantas.plantasCat_controller import plantasCat_router
from Controllers.Plagas.plagas_controller import plagas_router
from Controllers.PlagXPlants.plagxplants_controller import plagsxplants_router
from Controllers.Plantaciones.plantaciones_controller import plantaciones_router
from Controllers.Roles.roles_controller import roles_router
from Controllers.RecordatoriosCuidados.recordatorios_cuidados_controller import recordatorios_cuidados_router
from Controllers.SintomaPlanta.sintoma_planta_controller import sintoma_planta_router
from Controllers.Alertas.alertas_controller import alertas_router

routers = APIRouter()
router_list = [
    auth_router,
    plantas_router,
    plantasCat_router,
    plagas_router,
    plagsxplants_router,
    plantaciones_router,
    roles_router,
    recordatorios_cuidados_router,
    sintoma_planta_router,
    alertas_router,
]


for router in router_list:
    routers.include_router(router)