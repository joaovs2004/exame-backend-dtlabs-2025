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

class QueryParameters(BaseModel):
    server_ulid: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    sensor_type: Optional[str]
    aggregation: Optional[str]
