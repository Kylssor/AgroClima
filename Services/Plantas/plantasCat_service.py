import uuid
from Contracts.abc_generic_repository import AbcGenericRepository
from Helpers.uuid_helper import Uuid_helper
from Models.Plantas.plantas_Cat import Plantas_Cat
from Schemas.Plantas.plantasCat_schema import PlantasCat_schema 



class PlantasCat_service():
    
    def __init__(
        self,
        repository: AbcGenericRepository[Plantas_Cat]
    ):
        self.repository = repository

    def get_all(self)-> list[Plantas_Cat]:
        return self.repository.read_by_options()


    def get_by_id(self, id: uuid.UUID) -> Plantas_Cat:
        Uuid_helper.check_valid_uuid(id)
        
        return self.repository.read_by_id(id)


    def create(self, data: PlantasCat_schema) -> Plantas_Cat:
        entity = Plantas_Cat(
            name = data.name
        )

        return self.repository.add(entity)


    def update(self, data: PlantasCat_schema) -> Plantas_Cat:
        Uuid_helper.check_valid_uuid(data.id)
        
        entity = Plantas_Cat(
            id=data.id,
            name = data.name,
        )

        return self.repository.update(entity)


    def delete(self, id: uuid.UUID):
        Uuid_helper.check_valid_uuid(id)
        
        return self.repository.delete_by_id(id)