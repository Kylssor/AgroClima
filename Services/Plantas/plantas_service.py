import uuid
from Contracts.abc_generic_repository import AbcGenericRepository
from Helpers.uuid_helper import Uuid_helper
from Models.Plantas.plantas import Plantas
from Schemas.Plantas.plantas_schema import Plantas_schema


class Plantas_service():
    
    def __init__(
        self,
        repository: AbcGenericRepository[Plantas]
    ):
        self.repository = repository


    def get_all(self)-> list[Plantas]:
        return self.repository.read_by_options()


    def get_by_id(self, id: uuid.UUID) -> Plantas:
        Uuid_helper.check_valid_uuid(id)
        
        return self.repository.read_by_id(id)


    def create(self, data: Plantas_schema) -> Plantas:
        entity = Plantas(
            name = data.name,
            description=data.description,
            recom=data.recom,
            product_category_id=data.plantascat_id
        )

        return self.repository.add(entity)


    def update(self, data: Plantas_schema) -> Plantas:
        Uuid_helper.check_valid_uuid(data.id)
        
        entity = Plantas(
            id=data.id,
            name = data.name,
            description=data.description,
            recom=data.recom,
            product_category_id=data.plantascat_id
        )

        return self.repository.update(entity)


    def delete(self, id: uuid.UUID):
        Uuid_helper.check_valid_uuid(id)
        
        return self.repository.delete_by_id(id)