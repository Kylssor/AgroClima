from typing import Optional
import uuid
from pydantic import BaseModel, Field


class User_info_schema(BaseModel):
    id: Optional[uuid.UUID] = Field(primary_key=True, unique=True)
    name: str = Field(default=None, nullable=False, max_length= 45)
    last_name: str = Field(default=None, nullable=False)
    email: str = Field(default=None, nullable=False, max_length= 100)
    
    class Config:
        json_schema_extra = {
            "example":{
                "id": "g12bs01-sc24-o8h7-h85k-2g7jf2068d0s",
                "name": "Pepito",
                "last_name": "Perez",
                "email": "Pepito@example.com"
            }
        }