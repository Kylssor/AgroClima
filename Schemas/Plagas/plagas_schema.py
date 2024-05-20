from typing import Optional
import uuid
from pydantic import BaseModel, Field


class Plagas_schema(BaseModel):
    id: Optional[uuid.UUID] = Field(default=None, nullable=True)
    name: str = Field(default=None, nullable=False, max_length= 50)
    description: str = Field(default=None, nullable=False, max_length= 100)
    recom: str = Field(default=None, nullable=False)
    
    
    class Config:
        json_schema_extra = {
            "example":{
                "id": "7fa78f45-7529-6234-b6ch-7c546f67bfb8",
                "name": "Patógenos",
                "description": "on microorganismos, tales como virus, bacterias, hongos, protozoos y nematodos causantes de enfermedades en las plantas, que impactan en un 10% la producción mundial.",
                "recom": "Para combatirlos, se utilizan los desinfectantes y la esterilización.",
            }
        }