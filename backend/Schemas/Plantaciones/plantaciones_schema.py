from decimal import Decimal
import uuid
from pydantic import BaseModel, Field


class Plantaciones_schema(BaseModel):
    id: uuid.UUID = Field(default=None, nullable=True)
    latitude: Decimal =  Field(default=None, nullable=False)
    longitude: Decimal =  Field(default=None, nullable=False)
    plants_id: uuid.UUID = Field(default=None, nullable=False, foreign_key="plantas.id")
    name: str = Field(default=None, nullable=False, max_length= 50)
    
    
    class Config:
        json_schema_extra = {
            "example":{
                "latitude": "4.5982702",
                "longitude": "74.1357403",
                "name": "Arroz",
                "plants_id": "1fa45f85-7567-3454-b6ch-7m786b67bjb8"
            }
        }