import uuid
from Contracts.abc_generic_repository import AbcGenericRepository
from Helpers.uuid_helper import Uuid_helper
from Models.SintomaPlanta.sintoma_planta import Sintoma_Planta
from Schemas.SintomaPlanta.sintoma_planta_schema import SintomaPlanta_schema


class SintomaPlanta_service():

    def __init__(
        self,
        repository: AbcGenericRepository[Sintoma_Planta]
    ):
        self.repository = repository


    def get_all(self) -> list[Sintoma_Planta]:
        return self.repository.read_by_options()


    def get_by_id(self, id: uuid.UUID) -> Sintoma_Planta:
        Uuid_helper.check_valid_uuid(id)

        return self.repository.read_by_id(id)


    def get_by_planta(self, planta_id: uuid.UUID) -> list[Sintoma_Planta]:
        Uuid_helper.check_valid_uuid(planta_id)

        criterion = lambda: (Sintoma_Planta.planta_id == planta_id)
        return self.repository.read_by_options(criterion)


    def create(self, data: SintomaPlanta_schema) -> Sintoma_Planta:
        entity = Sintoma_Planta(
            planta_id=data.planta_id,
            sintoma=data.sintoma,
            diagnostico=data.diagnostico,
            recomendacion=data.recomendacion,
        )

        return self.repository.add(entity)


    def update(self, data: SintomaPlanta_schema) -> Sintoma_Planta:
        Uuid_helper.check_valid_uuid(data.id)

        entity = Sintoma_Planta(
            id=data.id,
            planta_id=data.planta_id,
            sintoma=data.sintoma,
            diagnostico=data.diagnostico,
            recomendacion=data.recomendacion,
        )

        return self.repository.update(entity)


    def delete(self, id: uuid.UUID):
        Uuid_helper.check_valid_uuid(id)

        return self.repository.delete_by_id(id)
