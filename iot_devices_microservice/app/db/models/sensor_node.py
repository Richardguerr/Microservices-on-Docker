from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db.session import Base

class SensorNode(Base):
    __tablename__ = "nodos_sensores"

    id = Column(String, primary_key=True)
    brand = Column(String, nullable=False)
    description = Column(String, nullable=False)
    associated_mine = Column(UUID(as_uuid=True), nullable=True)
    zone_category = Column(String, nullable=True)
    zone_name = Column(String, nullable=True)
    id_iot_gateway = Column(UUID(as_uuid=True), ForeignKey("iot_gateways.id"), nullable=True)
