
from sqlmodel import Field
from Models.Base.Base_model import Base_Model



class Plags(Base_Model, table=True):
    name: str = Field(default=None, nullable=False, max_length= 50)
    description: str = Field(default=None, nullable=False, max_length= 100)
    recomenda: str = Field(default=None, nullable=False)

    