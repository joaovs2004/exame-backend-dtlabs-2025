from typing import Annotated
from fastapi import HTTPException, Query
from sqlmodel import select
from app.db import session
from app.db.models import SensorData, Server
from app.models.data_models import Data, QueryParameters
from sqlalchemy import func

def create_sensor_data(data: Data, session: session.SessionDep):
    server_in_db = session.exec(select(Server).where(Server.server_id == data.server_ulid)).first()

    if not server_in_db:
        raise HTTPException(status_code=404, detail="Server is not in database")

    session.add(SensorData(
        server_id=data.server_ulid,
        timestamp=data.timestamp,
        temperature=data.temperature,
        humidity=data.humidity,
        voltage=data.voltage,
        current=data.current
    ))
    session.commit()

def get_sensor_data(query_parameters: Annotated[QueryParameters, Query()], session: session.SessionDep):
    query_values = query_parameters.model_dump()
    sensor_query = select(SensorData)
    sensor_data_values = []

    server_ulid = query_parameters.server_ulid
    start_time = query_parameters.start_time
    end_time = query_parameters.end_time
    sensor_type = query_parameters.sensor_type
    aggregation = query_parameters.aggregation

    if server_ulid:
        sensor_query = sensor_query.where(SensorData.server_id == query_parameters.server_ulid)

    if start_time:
        sensor_query = sensor_query.where(SensorData.timestamp >= start_time, SensorData.timestamp <= end_time)

    # If sensor_type is provided, get only rows with provided type
    if sensor_type:
        if sensor_type == "temperature":
            sensor_query = sensor_query.where(SensorData.temperature is not None)
        elif sensor_type == "humidity":
            sensor_query = sensor_query.where(SensorData.humidity is not None)
        elif sensor_type == "voltage":
            sensor_query = sensor_query.where(SensorData.voltage is not None)
        elif sensor_type == "current":
            sensor_query = sensor_query.where(SensorData.current is not None)

    if aggregation:
        truncated_timestamp = func.date_trunc(aggregation, SensorData.timestamp)
        sensor_query = select(
            truncated_timestamp.label("timestamp"),
            func.avg(SensorData.temperature).label("temperature"),
            func.avg(SensorData.humidity).label("humidity"),
            func.avg(SensorData.voltage).label("voltage"),
            func.avg(SensorData.current).label("current")
        ).group_by(truncated_timestamp).order_by(truncated_timestamp)


    sensor_data_values = session.exec(sensor_query).all()

    sensor_data = []

    for data in sensor_data_values:
        timestamp = data.timestamp if aggregation is None else data[0]

        if data.temperature is not None:
            sensor_data.append({
                "timestamp": timestamp,
                "temperature": data.temperature
            })
        if data.humidity is not None:
            sensor_data.append({
                "timestamp": timestamp,
                "humidity": data.humidity
            })
        if data.voltage is not None:
            sensor_data.append({
                "timestamp": timestamp,
                "voltage": data.voltage
            })
        if data.current is not None:
            sensor_data.append({
                "timestamp": timestamp,
                "current": data.current
            })

    filtered_sensor_data = []

    # Filter only select sensor_type if provided
    if sensor_type:
        for data in sensor_data:
            if data.get(sensor_type):
                filtered_sensor_data.append({
                    "timestamp": data.get("timestamp"),
                    sensor_type: data.get(sensor_type)
                })

        return filtered_sensor_data

    # Remove empty fields
    sensor_data = [
        {key: value for key, value in data.items() if value}
        for data in sensor_data
    ]
    return sensor_data