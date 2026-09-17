from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship
from Models.Base.Base_model import Base_Model

if TYPE_CHECKING:
    from Models.Plantas.plantas import Plantas

class Plantas_Cat(Base_Model, table=True):
    name: str = Field(default=None, nullable=False, max_length= 50)

    plantas: list["Plantas"] = Relationship(back_populates="plantas_Cat")