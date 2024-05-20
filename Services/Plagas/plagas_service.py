import uuid
from Contracts.abc_generic_repository import AbcGenericRepository
from Helpers.uuid_helper import Uuid_helper
from Models.Plagas.plagas import Plags
from Schemas.Plagas.plagas_schema import Plagas_schema


class Plagas_service():
    
    def __init__(
        self,
        repository: AbcGenericRepository[Plags]
    ):
        self.repository = repository


    def get_all(self)-> list[Plags]:
        return self.repository.read_by_options()


    def get_by_id(self, id: uuid.UUID) -> Plags:
        Uuid_helper.check_valid_uuid(id)
        
        return self.repository.read_by_id(id)


    def create(self, data: Plagas_schema) -> Plags:
        entity = Plags(
            name = data.name,
            description=data.description,
            recom=data.recom,
        )

        return self.repository.add(entity)


    def update(self, data: Plagas_schema) -> Plags:
        Uuid_helper.check_valid_uuid(data.id)
        
        entity = Plags(
            name = data.name,
            description=data.description,
            recom=data.recom,
        )

        return self.repository.update(entity)


    def delete(self, id: uuid.UUID):
        Uuid_helper.check_valid_uuid(id)
        
        return self.repository.delete_by_id(id)