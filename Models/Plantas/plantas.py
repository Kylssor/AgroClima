from typing import Optional
import uuid
from sqlmodel import Field, Relationship
from Models.Base.Base_model import Base_Model
from Models.Plantas.plantas_Cat import Plantas_Cat


class Plantas(Base_Model, table=True):
    name: str = Field(default=None, nullable=False, max_length= 50)
    description: str = Field(default=None, nullable=False, max_length= 100)
    recom: str = Field(default=None, nullable=False, max_length= 100)
    plantas_cat_id: uuid.UUID = Field(default=None, nullable=False, foreign_key="plantas_cat.id")

    Plantes_Cat: Optional[Plantas_Cat] = Relationship(back_populates="plantas")
    
