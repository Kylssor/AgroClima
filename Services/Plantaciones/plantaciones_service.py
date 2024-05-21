import uuid
from Contracts.abc_generic_repository import AbcGenericRepository
from Helpers.uuid_helper import Uuid_helper
from Models.Plantaciones.plantaciones import Plants_mp
from Schemas.Plantaciones.plantaciones_schema import Plantaciones_schema


class Plantaciones_service():
    
    def __init__(
        self,
        repository: AbcGenericRepository[Plants_mp]
    ):
        self.repository = repository


    def get_all(self)-> list[Plants_mp]:
        return self.repository.read_by_options()


    def get_by_id(self, id: uuid.UUID) -> Plants_mp:
        Uuid_helper.check_valid_uuid(id)
        
        return self.repository.read_by_id(id)


    def create(self, data: Plantaciones_schema) -> Plants_mp:
        entity = Plants_mp(
            latitude = data.latitude,
            longitude=data.longitude,
            name = data.name,
            plants_id=data.plants_id,
        )

        return self.repository.add(entity)


    def update(self, data: Plantaciones_schema) -> Plants_mp:
        Uuid_helper.check_valid_uuid(data.plants_id)
        
        entity = Plants_mp(
            latitude = data.latitude,
            longitude=data.longitude,
            name = data.name,
            plants_id=data.plants_id,
        )

        return self.repository.update(entity)


    def delete(self, id: uuid.UUID):
        Uuid_helper.check_valid_uuid(id)
        
        return self.repository.delete_by_id(id)