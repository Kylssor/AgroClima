"""Regresión: SqlAlchemyGenericRepository.add() hacía `self.entity = entity`,
sobrescribiendo la referencia a la clase del modelo con la instancia recién
creada. Cualquier lectura posterior con la misma instancia de repositorio
fallaba. Ver backend/Models/Repository/sqlalchemy_generic_repository.py.
"""
from Models.Plantas.plantas_Cat import Plantas_Cat


def test_add_no_corrompe_el_repositorio_para_lecturas_posteriores(repo_factory):
    repo = repo_factory(Plantas_Cat)

    repo.add(Plantas_Cat(name="Hortaliza"))

    # Antes del fix, esto lanzaba porque self.entity ya no era la clase
    # Plantas_Cat sino la instancia insertada.
    todas = repo.read_by_options()

    assert len(todas) == 1
    assert todas[0].name == "Hortaliza"


def test_add_luego_read_by_id_funciona(repo_factory):
    repo = repo_factory(Plantas_Cat)

    creada = repo.add(Plantas_Cat(name="Frutal"))
    leida = repo.read_by_id(creada.id)

    assert leida.id == creada.id
    assert leida.name == "Frutal"
