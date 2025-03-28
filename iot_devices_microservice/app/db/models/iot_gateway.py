from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from db.session import Base

class IoTGateway(Base):
    __tablename__ = "iot_gateways"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand = Column(String, nullable=False)
    description = Column(String, nullable=False)
