from typing import Optional
import uuid
from pydantic import BaseModel, Field


class Roles_schema(BaseModel):
    id: Optional[uuid.UUID] = Field(default=None, nullable=True, unique=True, )
    name: str = Field(default=None, nullable=False, max_length= 100)
    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")
    rolesty_id: uuid.UUID = Field(default=None, nullable=False, foreign_key="rolesty.id")
    
    class Config:
        json_schema_extra = {
            "example":{
                "id": "6fa74f23-9516-4462-b9ch-4c957f45bfb6",
                "name": "Admin",
                
            }
        }