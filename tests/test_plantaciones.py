"""Plantaciones: antes get_all/get_by_id no requerían sesión y create()
nunca asignaba el user_id dueño — cualquiera veía las plantaciones de
todos. Ver backend/Services/Plantaciones/plantaciones_service.py.
"""
import pytest

from Exceptions.unauthorized_exception import UnauthorizedException
from Models.Plantas.plantas import Plantas
from Models.Plantas.plantas_Cat import Plantas_Cat
from Models.Plantaciones.plantaciones import Plants_mp
from Models.User.user import User
from Schemas.Plantaciones.plantaciones_schema import Plantaciones_schema
from Services.Plantaciones.plantaciones_service import Plantaciones_service


@pytest.fixture()
def escenario(repo_factory):
    repo_user = repo_factory(User)
    repo_cat = repo_factory(Plantas_Cat)
    repo_planta = repo_factory(Plantas)
    repo_plantacion = repo_factory(Plants_mp)

    u1 = repo_user.add(User(name="Juan", last_name="Perez", email="juan@test.com", password="hash"))
    u2 = repo_user.add(User(name="Ana", last_name="Gomez", email="ana@test.com", password="hash"))
    cat = repo_cat.add(Plantas_Cat(name="Hortaliza"))
    planta = repo_planta.add(Plantas(name="Tomate", description="d", recom="r", plantas_cat_id=cat.id))

    service = Plantaciones_service(repo_plantacion)
    return {"service": service, "u1": u1, "u2": u2, "planta": planta}


def _crear_schema(planta_id, nombre="Mi tomate"):
    return Plantaciones_schema(direction="Finca 1", latitude=1, longitude=1, plants_id=planta_id, name=nombre)


def test_crear_plantacion_asigna_el_usuario_dueno(escenario):
    service, u1, planta = escenario["service"], escenario["u1"], escenario["planta"]

    creada = service.create(_crear_schema(planta.id), u1.id)

    assert creada.user_id == u1.id


def test_get_all_solo_devuelve_las_del_usuario_autenticado(escenario):
    service, u1, u2, planta = escenario["service"], escenario["u1"], escenario["u2"], escenario["planta"]
    service.create(_crear_schema(planta.id), u1.id)

    assert service.get_all(u2.id) == []
    assert len(service.get_all(u1.id)) == 1


def test_get_by_id_bloquea_acceso_a_plantacion_ajena(escenario):
    service, u1, u2, planta = escenario["service"], escenario["u1"], escenario["u2"], escenario["planta"]
    creada = service.create(_crear_schema(planta.id), u1.id)

    with pytest.raises(UnauthorizedException):
        service.get_by_id(creada.id, u2.id)

    # El dueño sí puede.
    assert service.get_by_id(creada.id, u1.id).id == creada.id


def test_delete_bloquea_borrar_plantacion_ajena(escenario):
    service, u1, u2, planta = escenario["service"], escenario["u1"], escenario["u2"], escenario["planta"]
    creada = service.create(_crear_schema(planta.id), u1.id)

    with pytest.raises(UnauthorizedException):
        service.delete(creada.id, u2.id)
