from pydantic import BaseModel
import uuid

class IoTGatewayBase(BaseModel):
    brand: str
    description: str

class IoTGatewayCreate(IoTGatewayBase):
    pass

class IoTGatewayResponse(IoTGatewayBase):
    id: uuid.UUID

    class Config:
        from_attributes = True
