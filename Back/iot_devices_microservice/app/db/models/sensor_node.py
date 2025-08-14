# db/models.py
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from app.db.session import Base

class SensorNode(Base):
    __tablename__ = "nodos_sensores"

    id = Column(String, primary_key=True)
    brand = Column(String, nullable=False)
    description = Column(String, nullable=False)
    zone_category = Column(String, nullable=True)
    zone_name = Column(String, nullable=True)
    id_iot_gateway = Column(UUID, ForeignKey('iot_gateways.id', ondelete='CASCADE')) 
    # Relaciones
    iot_gateway = relationship("IoTGateway", back_populates="sensor_nodes")
    sensors = relationship("Sensor", back_populates="sensor_node", cascade="all, delete-orphan",passive_deletes=True)  # Añadir esto para mejor rendimiento