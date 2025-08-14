# db/models.py
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from app.db.session import Base

class IoTGateway(Base):
    __tablename__ = "iot_gateways"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))   
    associated_mine = Column(UUID(as_uuid=True), nullable=True)
    brand = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    # Relación con nodos sensores
    sensor_nodes = relationship("SensorNode", back_populates="iot_gateway",cascade="all, delete-orphan",passive_deletes=True)