from typing import Annotated
from fastapi import APIRouter, Query

from app.db import session
from app.models.data_models import Data, QueryParameters
from app.services.data_services import create_sensor_data

router = APIRouter()

@router.post("/data", tags=["data"])
def send_data(data: Data, session: session.SessionDep):
    create_sensor_data(data, session)
    return {"message": "Sensor data created"}

@router.get("/data", tags=["data"])
def get_data(queryParameters: Annotated[QueryParameters, Query()]):
    return {"message": "ok"}
