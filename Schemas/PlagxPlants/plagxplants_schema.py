
from typing import Optional
import uuid
from pydantic import BaseModel, Field


class PlagxPlants_schema(BaseModel):
    Plagas_id: Optional[uuid.UUID] = Field(default=None, nullable=True)
    Plantas_id: uuid.UUID = Field(default=None, nullable=False)
    
    class Config:
        json_schema_extra = {
            "example":{
                "plagas_id": "7fa78f45-7529-6234-b6ch-7c546f67bfb8",
                "plantas_id": "6fa74f23-9516-4462-b9ch-4c957f45bfb6"
            }
        }