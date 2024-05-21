import uuid
from Contracts.abc_generic_repository import AbcGenericRepository
from Helpers.uuid_helper import Uuid_helper
from Models.Roles.roles import Roles
from Schemas.Roles.roles_schema import Roles_schema


class Roles_service():
    
    def __init__(
        self,
        repository: AbcGenericRepository[Roles]
    ):
        self.repository = repository


    def get_all(self)-> list[Roles]:
        return self.repository.read_by_options()


    def get_by_id(self, id: uuid.UUID) -> Roles:
        Uuid_helper.check_valid_uuid(id)
        
        return self.repository.read_by_id(id)


    def create(self, data: Roles_schema) -> Roles:
        entity = Roles(
            name = data.name,
            user=data.user_id,
            rolesty=data.rolesty_id
        )

        return self.repository.add(entity)


    def update(self, data: Roles_schema) -> Roles:
        Uuid_helper.check_valid_uuid(data.id)
        
        entity = Roles(
            id=data.id,
            name = data.name,
            user=data.user_id,
            rolesty=data.rolesty_id
        )

        return self.repository.update(entity)


    def delete(self, id: uuid.UUID):
        Uuid_helper.check_valid_uuid(id)
        
        return self.repository.delete_by_id(id)