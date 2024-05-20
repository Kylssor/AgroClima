from typing import Optional
import uuid
from pydantic import BaseModel, Field


class PlantasCat_schema(BaseModel):
    id: Optional[uuid.UUID] = Field(default=None, nullable=True)
    name: str = Field(default=None, nullable=False, max_length= 50)
    
    class Config:
        json_schema_extra = {
            "example":{
                "id": "6fa74f23-9516-4462-b9ch-4c957f45bfb6",
                "name": "Granos",
            }
        }