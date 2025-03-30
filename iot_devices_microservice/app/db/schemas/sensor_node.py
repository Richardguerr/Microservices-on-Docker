from pydantic import BaseModel, Field
from typing import Optional, List, Generic
import uuid
from app.db.schemas.sensor import SensorResponse


class SensorNodeBase(BaseModel):
    id:str
    brand: str
    description: str
    zone_category: Optional[str] = None
    zone_name: Optional[str] = None
    id_iot_gateway: Optional[uuid.UUID] = None

class SensorNodeCreate(SensorNodeBase):
    id: str = Field(..., min_length=1, description="ID único del nodo sensor")

class SensorNodeUpdate(BaseModel):
    brand: Optional[str] = None
    description: Optional[str] = None
    zone_category: Optional[str] = None
    zone_name: Optional[str] = None
    id_iot_gateway: Optional[uuid.UUID] = None

class SensorNodeResponse(SensorNodeBase):
    sensors: List[SensorResponse] = []  # Lista de sensores asociados
    
    class Config:
        from_attributes = True

class PaginatedResponse(BaseModel):
    total: int
    page: int
    per_page: int
    items: List[SensorNodeResponse]