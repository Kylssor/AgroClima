from pydantic import BaseModel, Field


class Sign_in_schema(BaseModel):
    email: str = Field(default=None, nullable=False, max_length= 100)
    password: str = Field(default=None, nullable=False)
    
    class Config:
        json_schema_extra = {
            "example":{
                "email": "Pepito@example.com",
                "password": "&i&hk@mjw785ym4ex#rmp6oct7rb#ii!isbu^@uay6g&yqj3z8",
            }
        }