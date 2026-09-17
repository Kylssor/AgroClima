"""SintomaPlanta: ficha de síntomas/recomendaciones por tipo de planta
(nueva entidad, ver SPEC.md)."""
from Models.Plantas.plantas import Plantas
from Models.Plantas.plantas_Cat import Plantas_Cat
from Models.SintomaPlanta.sintoma_planta import Sintoma_Planta
from Schemas.SintomaPlanta.sintoma_planta_schema import SintomaPlanta_schema
from Services.SintomaPlanta.sintoma_planta_service import SintomaPlanta_service


def _crear_planta(repo_factory):
    cat = repo_factory(Plantas_Cat).add(Plantas_Cat(name="Hortaliza"))
    return repo_factory(Plantas).add(Plantas(name="Tomate", description="d", recom="r", plantas_cat_id=cat.id))


def test_crear_y_consultar_sintoma(repo_factory):
    planta = _crear_planta(repo_factory)
    service = SintomaPlanta_service(repo_factory(Sintoma_Planta))

    creado = service.create(SintomaPlanta_schema(
        planta_id=planta.id,
        sintoma="Hojas amarillas",
        diagnostico="Exceso de riego",
        recomendacion="Reducir la frecuencia de riego",
    ))

    assert service.get_by_id(creado.id).sintoma == "Hojas amarillas"


def test_get_by_planta_filtra_solo_los_de_esa_planta(repo_factory):
    planta1 = _crear_planta(repo_factory)
    planta2 = _crear_planta(repo_factory)
    service = SintomaPlanta_service(repo_factory(Sintoma_Planta))

    service.create(SintomaPlanta_schema(
        planta_id=planta1.id, sintoma="Hojas amarillas", diagnostico="d", recomendacion="r",
    ))
    service.create(SintomaPlanta_schema(
        planta_id=planta2.id, sintoma="Manchas negras", diagnostico="d", recomendacion="r",
    ))

    resultado = service.get_by_planta(planta1.id)

    assert len(resultado) == 1
    assert resultado[0].sintoma == "Hojas amarillas"
