import uuid
from sqlmodel import Field
from Models.Base.Base_model import Base_Model


class Sintoma_Planta(Base_Model, table=True):
    planta_id: uuid.UUID = Field(default=None, nullable=False, foreign_key="plantas.id")
    sintoma: str = Field(default=None, nullable=False, max_length=100)
    diagnostico: str = Field(default=None, nullable=False, max_length=200)
    recomendacion: str = Field(default=None, nullable=False)
