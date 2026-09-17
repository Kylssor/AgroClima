from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class RecordatorioCuidado_schema(BaseModel):
    id: Optional[uuid.UUID] = Field(default=None, nullable=True)
    plantacion_id: uuid.UUID = Field(default=None, nullable=False)
    tipo_cuidado: str = Field(default=None, nullable=False, max_length=50)
    frecuencia_dias: int = Field(default=None, nullable=False)
    proxima_fecha: Optional[datetime] = Field(default=None, nullable=True)


    class Config:
        json_schema_extra = {
            "example": {
                "plantacion_id": "7fa78f45-7529-6234-b6ch-7c546f67bfb8",
                "tipo_cuidado": "riego",
                "frecuencia_dias": 3,
            }
        }
