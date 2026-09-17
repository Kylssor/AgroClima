import uuid
from Contracts.abc_generic_repository import AbcGenericRepository
from Helpers.uuid_helper import Uuid_helper
from Models.PlagXPlants.plagxplants import Plagsxplants
from Schemas.PlagxPlants.plagxplants_schema import PlagxPlants_schema


class Plagxplants_service():
    
    def __init__(
        self,
        repository: AbcGenericRepository[Plagsxplants]
    ):
        self.repository = repository


    def get_all(self)-> list[Plagsxplants]:
        return self.repository.read_by_options()


    def get_by_id(self, id: uuid.UUID) -> Plagsxplants:
        Uuid_helper.check_valid_uuid(id)
        
        return self.repository.read_by_id(id)


    def create(self, data: PlagxPlants_schema) -> Plagsxplants:
        entity = Plagsxplants(
            plagas_id=data.plagas_id,
            plantas_id=data.plantas_id
        )

        return self.repository.add(entity)


    def update(self, data: PlagxPlants_schema) -> Plagsxplants:
        Uuid_helper.check_valid_uuid(data.id)
        
        entity = Plagsxplants(
            id=data.id,
            plagas_id=data.plagas_id,
            plantas_id=data.plantas_id
        )

        return self.repository.update(entity)


    def delete(self, id: uuid.UUID):
        Uuid_helper.check_valid_uuid(id)
        
        return self.repository.delete_by_id(id)