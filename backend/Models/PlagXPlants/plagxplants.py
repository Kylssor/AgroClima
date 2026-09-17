
import uuid
from sqlmodel import Field

from Models.Base.Base_model import Base_Model


class Plagsxplants(Base_Model, table=True):
    Plantas_id: uuid.UUID = Field(default=None, nullable=False, foreign_key="plantas.id")
    Plags_id: uuid.UUID = Field(default=None, nullable=False, foreign_key="plags.id")

   