
import uuid
from datetime import datetime
from sqlmodel import Field
from Models.Base.Base_model import Base_Model



class RecordCui(Base_Model, table=True):
    plantacion_id: uuid.UUID = Field(default=None, nullable=False, foreign_key="plants_mp.id")
    tipo_cuidado: str = Field(default=None, nullable=False, max_length=50)
    frecuencia_dias: int = Field(default=None, nullable=False)
    proxima_fecha: datetime = Field(default=None, nullable=False)
    activo: bool = Field(default=None, nullable=False)