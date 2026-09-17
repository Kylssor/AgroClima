from decimal import Decimal
import uuid
from sqlmodel import Field

from Models.Base.Base_model import Base_Model


class Plants_mp(Base_Model, table=True):
    direction: str = Field(default=None, nullable=False, max_length= 100)
    latitude: Decimal =  Field(default=None, nullable=False)
    longitude: Decimal =  Field(default=None, nullable=False)
    plants_id: uuid.UUID = Field(default=None, nullable=False, foreign_key="plantas.id")
    user_id: uuid.UUID = Field(default=None, nullable=False, foreign_key="user.id")

   