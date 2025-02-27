from pydantic import BaseModel, Field

class NewServer(BaseModel):
    name: str = Field(min_length=4)