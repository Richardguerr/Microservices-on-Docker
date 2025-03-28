from pydantic import BaseModel
from typing import Optional
import uuid

class SensorBase(BaseModel):
    variable: str
    marca: str
    referencia: str

class SensorCreate(SensorBase):
    id_node: Optional[str] = None

class SensorResponse(SensorBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
