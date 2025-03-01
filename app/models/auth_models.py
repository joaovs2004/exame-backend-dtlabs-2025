from pydantic import BaseModel, Field

class NewUser(BaseModel):
    name: str = Field(min_length=3)
    password: str = Field(min_length=3)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    name: str | None = None