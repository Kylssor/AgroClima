from typing import Optional
import uuid
from sqlmodel import Field, Relationship

from Models.Base.Base_model import Base_Model
from Models.Roles.rolesTy import RolesTy



class Roles(Base_Model, table=True):
    name: str = Field(default=None, nullable=False, max_length= 100)
    rolesty_id: uuid.UUID = Field(default=None, nullable=False, foreign_key="rolesty.id")

    rolesTy: Optional[RolesTy] = Relationship(back_populates="roles")
 