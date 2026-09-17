
import uuid
from datetime import datetime
from sqlmodel import Field
from Models.Base.Base_model import Base_Model



class RecordCui(Base_Model, table=True):
    fecha_hora: datetime =  Field(default=None, nullable=False)
    record: str = Field(default=None, nullable=False, max_length= 100)
    Plantas_id: uuid.UUID = Field(default=None, nullable=False, foreign_key="plantas.id")