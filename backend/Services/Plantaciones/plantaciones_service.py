import uuid
from Contracts.abc_generic_repository import AbcGenericRepository
from Exceptions.unauthorized_exception import UnauthorizedException
from Helpers.uuid_helper import Uuid_helper
from Models.Plantaciones.plantaciones import Plants_mp
from Schemas.Plantaciones.plantaciones_schema import Plantaciones_schema


class Plantaciones_service():

    def __init__(
        self,
        repository: AbcGenericRepository[Plants_mp]
    ):
        self.repository = repository


    def get_all(self, user_id: uuid.UUID)-> list[Plants_mp]:
        criterion = lambda: (Plants_mp.user_id == user_id)
        return self.repository.read_by_options(criterion)


    def get_by_id(self, id: uuid.UUID, user_id: uuid.UUID) -> Plants_mp:
        Uuid_helper.check_valid_uuid(id)

        plantacion = self.repository.read_by_id(id)
        self._check_ownership(plantacion, user_id)
        return plantacion


    def create(self, data: Plantaciones_schema, user_id: uuid.UUID) -> Plants_mp:
        entity = Plants_mp(
            direction=data.direction,
            latitude = data.latitude,
            longitude=data.longitude,
            name = data.name,
            plants_id=data.plants_id,
            user_id=user_id,
        )

        return self.repository.add(entity)


    def update(self, data: Plantaciones_schema, user_id: uuid.UUID) -> Plants_mp:
        Uuid_helper.check_valid_uuid(data.id)

        plantacion = self.repository.read_by_id(data.id)
        self._check_ownership(plantacion, user_id)

        entity = Plants_mp(
            id=data.id,
            direction=data.direction,
            latitude = data.latitude,
            longitude=data.longitude,
            name = data.name,
            plants_id=data.plants_id,
        )

        return self.repository.update(entity)


    def delete(self, id: uuid.UUID, user_id: uuid.UUID):
        Uuid_helper.check_valid_uuid(id)

        plantacion = self.repository.read_by_id(id)
        self._check_ownership(plantacion, user_id)

        return self.repository.delete_by_id(id)


    def _check_ownership(self, plantacion: Plants_mp, user_id: uuid.UUID) -> None:
        if plantacion.user_id != user_id:
            raise UnauthorizedException("Esta plantación no te pertenece.")
