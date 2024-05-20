from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship

from Models.Base.Base_model import Base_Model

if TYPE_CHECKING:
    from Models.Roles.roles import Roles


class RolesTy(Base_Model, table=True):
    name: str = Field(default=None, nullable=False, max_length= 100)

    roles: list["Roles"] = Relationship(back_populates="rolesTy")