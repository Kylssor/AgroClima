from typing import Optional
import uuid
from pydantic import BaseModel, Field


class Plantas_schema(BaseModel):
    id: Optional[uuid.UUID] = Field(default=None, nullable=True, unique=True, )
    name: str = Field(default=None, nullable=False, max_length= 50)
    description: str = Field(default=None, nullable=False, max_length= 100)
    recom: str = Field(default=None, nullable=False)
    plantascat_id: uuid.UUID = Field(default=None, nullable=False)
    
    class Config:
        json_schema_extra = {
            "example":{
                "id": "6fa74f23-9516-4462-b9ch-4c957f45bfb6",
                "name": "Maiz",
                "description": "El maíz es una planta alta que puede alcanzar hasta 3 metros de altura. Tiene tallos largos y robustos, hojas largas y lanceoladas, y flores masculinas y femeninas separadas.",
                "recom": "El tiene diferentes ciclos de maduración, desde cortos (Noventa-Cien días) hasta largos (Ciento treinta-Ciento Cuarenta días). Es importante elegir un ciclo adecuado para la región donde se va a cultivar.",
                "plantascat_id": "6fa74f23-9516-4462-b9ch-4c957f45bfb6"
            }
        }