from sqlmodel import Field, SQLModel
from datetime import datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    name: str = Field(index=True, unique=True)
    password: str | None = Field(default=None, index=True)

class Server(SQLModel, table=True):
    server_id: str = Field(index=True, primary_key=True)
    name: str = Field(default=None, index=True)

class SensorData(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True, index=True)
    server_id: str = Field(default=None, foreign_key="server.server_id")
    timestamp: datetime = Field(default=None, index=True)
    temperature: float | None = Field(default=None, index=True)
    humidity: float | None = Field(default=None, index=True)
    voltage: float | None = Field(default=None, index=True)
    current: float | None = Field(default=None, index=True)