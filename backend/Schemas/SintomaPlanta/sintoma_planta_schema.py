from typing import Optional
import uuid
from pydantic import BaseModel, Field


class SintomaPlanta_schema(BaseModel):
    id: Optional[uuid.UUID] = Field(default=None, nullable=True)
    planta_id: uuid.UUID = Field(default=None, nullable=False)
    sintoma: str = Field(default=None, nullable=False, max_length=100)
    diagnostico: str = Field(default=None, nullable=False, max_length=200)
    recomendacion: str = Field(default=None, nullable=False)


    class Config:
        json_schema_extra = {
            "example": {
                "planta_id": "7fa78f45-7529-6234-b6ch-7c546f67bfb8",
                "sintoma": "Hojas amarillas",
                "diagnostico": "Posible falta de nitrógeno o exceso de riego",
                "recomendacion": "Reduce la frecuencia de riego y aplica un fertilizante rico en nitrógeno",
            }
        }
