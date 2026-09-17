"""Regresión: el modelo Plags tenía un campo `recomenda` que no coincidía
con la columna real `recom` (usada por la migración, el schema y el
service). Crear una plaga guardaba `recomenda=None` y violaba el NOT NULL.
Ver backend/Models/Plagas/plagas.py.
"""
from Models.Plagas.plagas import Plags
from Schemas.Plagas.plagas_schema import Plagas_schema
from Services.Plagas.plagas_service import Plagas_service


def test_crear_plaga_guarda_la_recomendacion(repo_factory):
    service = Plagas_service(repo_factory(Plags))

    creada = service.create(Plagas_schema(
        name="Pulgón",
        description="Insecto que ataca los brotes tiernos.",
        recom="Usar jabón potásico o liberar mariquitas.",
    ))

    assert creada.recom == "Usar jabón potásico o liberar mariquitas."

    leida = service.get_by_id(creada.id)
    assert leida.recom == "Usar jabón potásico o liberar mariquitas."
