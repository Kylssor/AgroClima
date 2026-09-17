"""RecordatoriosCuidados (antes solo existía el modelo, sin service ni
controller) y GET /Alertas: ownership por plantación, recálculo de
proxima_fecha al marcar cumplido, y filtrado de vencidos/próximos.
"""
from datetime import datetime, timedelta, timezone

import pytest

from Exceptions.unauthorized_exception import UnauthorizedException
from Models.Plantas.plantas import Plantas
from Models.Plantas.plantas_Cat import Plantas_Cat
from Models.Plantaciones.plantaciones import Plants_mp
from Models.RecordatoriosCuidados.recordCui import RecordCui
from Models.User.user import User
from Schemas.Plantaciones.plantaciones_schema import Plantaciones_schema
from Schemas.RecordatoriosCuidados.recordatorio_cuidado_schema import RecordatorioCuidado_schema
from Services.Plantaciones.plantaciones_service import Plantaciones_service
from Services.RecordatoriosCuidados.recordatorio_cuidado_service import RecordatorioCuidado_service


@pytest.fixture()
def escenario(repo_factory):
    repo_user = repo_factory(User)
    repo_cat = repo_factory(Plantas_Cat)
    repo_planta = repo_factory(Plantas)
    repo_plantacion = repo_factory(Plants_mp)
    repo_record = repo_factory(RecordCui)

    u1 = repo_user.add(User(name="Juan", last_name="Perez", email="juan@test.com", password="hash"))
    u2 = repo_user.add(User(name="Ana", last_name="Gomez", email="ana@test.com", password="hash"))
    cat = repo_cat.add(Plantas_Cat(name="Hortaliza"))
    planta = repo_planta.add(Plantas(name="Tomate", description="d", recom="r", plantas_cat_id=cat.id))

    plantaciones_service = Plantaciones_service(repo_plantacion)
    plantacion = plantaciones_service.create(
        Plantaciones_schema(direction="Finca 1", latitude=1, longitude=1, plants_id=planta.id, name="Mi tomate"),
        u1.id,
    )

    recordatorios_service = RecordatorioCuidado_service(repo_record, repo_plantacion)

    return {
        "recordatorios": recordatorios_service,
        "repo_record": repo_record,
        "u1": u1,
        "u2": u2,
        "plantacion": plantacion,
    }


def test_crear_recordatorio_calcula_proxima_fecha(escenario):
    service, plantacion, u1 = escenario["recordatorios"], escenario["plantacion"], escenario["u1"]

    antes = datetime.now(timezone.utc)
    creado = service.create(
        RecordatorioCuidado_schema(plantacion_id=plantacion.id, tipo_cuidado="riego", frecuencia_dias=3),
        u1.id,
    )

    assert creado.activo is True
    assert creado.proxima_fecha.replace(tzinfo=timezone.utc) >= antes + timedelta(days=3) - timedelta(minutes=1)


def test_crear_recordatorio_bloquea_plantacion_ajena(escenario):
    service, plantacion, u2 = escenario["recordatorios"], escenario["plantacion"], escenario["u2"]

    with pytest.raises(UnauthorizedException):
        service.create(
            RecordatorioCuidado_schema(plantacion_id=plantacion.id, tipo_cuidado="riego", frecuencia_dias=1),
            u2.id,
        )


def test_alertas_solo_incluye_lo_del_usuario_dueno(escenario):
    service = escenario["recordatorios"]
    repo_record = escenario["repo_record"]
    plantacion, u1, u2 = escenario["plantacion"], escenario["u1"], escenario["u2"]

    creado = service.create(
        RecordatorioCuidado_schema(plantacion_id=plantacion.id, tipo_cuidado="riego", frecuencia_dias=3),
        u1.id,
    )
    vencido = RecordCui(id=creado.id, proxima_fecha=datetime.now(timezone.utc) - timedelta(days=1))
    repo_record.update(vencido)

    assert len(service.get_alertas(u1.id)) == 1
    assert service.get_alertas(u2.id) == []


def test_marcar_cumplido_reprograma_y_sale_de_vencidos(escenario):
    service = escenario["recordatorios"]
    repo_record = escenario["repo_record"]
    plantacion, u1 = escenario["plantacion"], escenario["u1"]

    creado = service.create(
        RecordatorioCuidado_schema(plantacion_id=plantacion.id, tipo_cuidado="riego", frecuencia_dias=3),
        u1.id,
    )
    vencido = RecordCui(id=creado.id, proxima_fecha=datetime.now(timezone.utc) - timedelta(days=1))
    repo_record.update(vencido)
    assert len(service.get_alertas(u1.id, dias_proximos=0)) == 1

    service.marcar_cumplido(creado.id, u1.id)

    assert service.get_alertas(u1.id, dias_proximos=0) == []
    # Pero sigue como "próximo" dentro de la ventana de frecuencia_dias.
    assert len(service.get_alertas(u1.id, dias_proximos=3)) == 1


def test_marcar_cumplido_bloquea_recordatorio_de_plantacion_ajena(escenario):
    service = escenario["recordatorios"]
    plantacion, u1, u2 = escenario["plantacion"], escenario["u1"], escenario["u2"]

    creado = service.create(
        RecordatorioCuidado_schema(plantacion_id=plantacion.id, tipo_cuidado="riego", frecuencia_dias=3),
        u1.id,
    )

    with pytest.raises(UnauthorizedException):
        service.marcar_cumplido(creado.id, u2.id)
