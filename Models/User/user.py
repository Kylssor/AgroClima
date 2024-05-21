
import uuid
from sqlmodel import Field
from Models.Base.Base_model import Base_Model


class User(Base_Model, table=True):
    id: uuid.UUID = Field(default=None, nullable=False, primary_key=True)
    name: str = Field(default=None, nullable=False, max_length= 50)
    last_name: str = Field(default=None, nullable=False)
    email: str = Field(default=None, nullable=False, max_length= 100)
    password: str = Field(default=None, nullable=False, max_length= 255)
    roles: uuid.UUID = Field(default=None, nullable=False, foreign_key="roles.id")
    
   