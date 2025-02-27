from sqlmodel import Field, Session, SQLModel, create_engine, select

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True, primary_key=True)
    password: str | None = Field(default=None, index=True)