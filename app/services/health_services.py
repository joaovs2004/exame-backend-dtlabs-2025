from fastapi import HTTPException
from sqlmodel import select
from app.db import session
from app.db.models import SensorData, Server
from datetime import datetime

def check_server_status(server_id, all, session: session.SessionDep):
    server = session.exec(select(Server).where(Server.server_id == server_id)).first()

    if not server and not all:
        raise HTTPException(status_code=404, detail="Server is not in database")
    elif not server and all:
        return {"server_ulid": server_id, "status": "offline", "server_name": server.name}

    sensor_data = session.exec(select(SensorData).where(SensorData.server_id == server_id).order_by(SensorData.timestamp)).all()
    server_status = "online"

    if not sensor_data:
        server_status = "offline"
    else:
        timestamp = sensor_data[0].timestamp
        time_difference = datetime.now() - timestamp

        if time_difference.total_seconds() > 10:
            server_status = "offline"

    return {"server_ulid": server_id, "status": server_status, "server_name": server.name}

def get_all_health(session: session.SessionDep):
    # sensor_data = session.exec(select(SensorData).where(SensorData.server_id == server_id).order_by(SensorData.timestamp)).all()
    servers = session.exec(select(Server)).all()
    # servers = session.exec(select(SensorData).order_by(SensorData.timestamp).distinct()).all()

    servers_data = []

    for server in servers:
        response = check_server_status(server.server_id, True, session)
        servers_data.append(response)

    return servers_data

def get_server_health_by_id(server_id: int, session: session.SessionDep):
    response = check_server_status(server_id, False, session)

    return response