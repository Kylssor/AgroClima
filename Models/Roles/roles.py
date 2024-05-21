from typing import Optional
import uuid
from sqlmodel import Field, Relationship

from Models.Base.Base_model import Base_Model
from Models.Roles.rolesTy import RolesTy
from Models.User.user import User



class Roles(Base_Model, table=True):

    name: str = Field(default=None, nullable=False, max_length= 100)
    user_id: uuid.UUID = Field(default=None, foreign_key="user.id")
    rolesty_id: uuid.UUID = Field(default=None, nullable=False, foreign_key="rolesty.id")


    roles_Ty: Optional[RolesTy] = Relationship(back_populates="roles")
 