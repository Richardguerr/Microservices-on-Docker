from pydantic import BaseModel
from typing import Optional
import uuid

class SensorNodeBase(BaseModel):
    id: str
    brand: str
    description: str
    associated_mine: Optional[uuid.UUID] = None
    zone_category: Optional[str] = None
    zone_name: Optional[str] = None
    id_iot_gateway: Optional[uuid.UUID] = None

class SensorNodeCreate(SensorNodeBase):
    pass

class SensorNodeResponse(SensorNodeBase):
    class Config:
        from_attributes = True
