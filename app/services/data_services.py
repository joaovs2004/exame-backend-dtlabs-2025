from fastapi import HTTPException
from sqlmodel import select
from app.db import session
from app.db.models import SensorData, Server
from app.models.data_models import Data

def create_sensor_data(data: Data, session: session.SessionDep):
    server_in_db = session.exec(select(Server).where(Server.server_id == data.server_ulid)).first()

    if not server_in_db:
        raise HTTPException(status_code=404, detail="Server is not in database")

    session.add(SensorData(
        server_id=data.server_ulid,
        timestamp=data.timestamp,
        temperature=data.temperature,
        voltage=data.voltage,
        current=data.current
    ))
    session.commit()