from typing import Annotated
from fastapi import APIRouter, Depends, Query

from app.db import session
from app.db.models import User
from app.models.data_models import Data, QueryParameters
from app.services.auth_services import get_current_user
from app.services.data_services import create_sensor_data, get_sensor_data

router = APIRouter()

@router.post("/data", tags=["data"])
async def send_data(data: Data, session: session.SessionDep):
    create_sensor_data(data, session)
    return {"message": "Sensor data created"}

@router.get("/data", tags=["data"])
async def get_data(
    user: Annotated[User, Depends(get_current_user)],
    query_parameters: Annotated[QueryParameters, Query()],
    session: session.SessionDep
    ):
    sensor_data = get_sensor_data(query_parameters, session)
    return sensor_data