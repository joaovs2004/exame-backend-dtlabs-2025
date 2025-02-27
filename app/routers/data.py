from fastapi import APIRouter
from pydantic import BaseModel


router = APIRouter()

class Data(BaseModel):
    server_ulid: str
    timestamp: str
    temperature: float
    humidity: float
    voltage: float
    current: float

@router.post("/data", tags=["data"])
def send_data(data: Data):
    return {"message": "ok"}

@router.get("/data", tags=["data"])
def get_data():
    return {"message": "ok"}
