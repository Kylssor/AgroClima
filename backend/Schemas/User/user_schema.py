from pydantic import BaseModel, Field


class User_schema(BaseModel):
    name: str = Field(default=None, nullable=False, max_length= 45)
    last_name: str = Field(default=None, nullable=False)
    email: str = Field(default=None, nullable=False, max_length= 100)
    password: str = Field(default=None, nullable=False)
    
    class Config:
        json_schema_extra = {
            "example":{
                "name": "Pepito",
                "last_name": "Perez",
                "email": "Pepito@example.com",
                "password": "&i&hk@mjw785ym4ex#rmp6oct7rb#ii!isbu^@uay6g&yqj3z8",
            }
        }