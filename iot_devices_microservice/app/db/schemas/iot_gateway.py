from pydantic import BaseModel
import uuid
from typing import List, Optional
from app.db.schemas.sensor_node import SensorNodeResponse
from app.db.schemas.sensor_node import SensorNodeCreate

class IoTGatewayBase(BaseModel):
    brand: str
    description: str
    associated_mine: Optional[uuid.UUID] = None


class IoTGatewayCreate(IoTGatewayBase):
    pass

class IoTGatewayResponse(IoTGatewayBase):
    id: uuid.UUID
    sensor_nodes: List[SensorNodeResponse] = []

    class Config:
        from_attributes = True
# db/schemas.py
class IoTGatewayUpdate(BaseModel):
    brand: Optional[str] = None
    description: Optional[str] = None
    associated_mine: Optional[uuid.UUID] = None


    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: List[IoTGatewayResponse]