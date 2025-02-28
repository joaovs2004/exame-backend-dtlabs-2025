from enum import Enum
from pydantic import BaseModel, model_validator
from datetime import datetime
from typing import Optional

class Data(BaseModel):
    server_ulid: str
    timestamp: datetime
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    voltage: Optional[float] = None
    current: Optional[float] = None

    @model_validator(mode="after")
    def check_sensor_values(self):
        if self.temperature is None and self.humidity is None and self.voltage is None and self.current is None:
            raise ValueError("At least one sensor value must be included")

        return self

class Aggregation(str, Enum):
    minute = "minute"
    hour = "hour"
    day = "day"

class SensorTypes(str, Enum):
    temperature = "temperature"
    humidity = "humidity"
    voltage = "voltage"
    current = "current"

class QueryParameters(BaseModel):
    server_ulid: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    sensor_type: Optional[SensorTypes] = None
    aggregation: Optional[Aggregation] = None

    @model_validator(mode="after")
    def validate_query_parameters(self):
        if self.start_time is not None and self.end_time is None:
            raise ValueError("end_time must be provided when start_time is specified")

        return self
