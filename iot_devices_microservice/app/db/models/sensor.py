from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from db.session import Base

class Sensor(Base):
    __tablename__ = "sensores"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_node = Column(String, ForeignKey("nodos_sensores.id"), nullable=True)
    variable = Column(String, nullable=False)
    marca = Column(String, nullable=False)
    referencia = Column(String, nullable=False)
    unidad_medicion = Column(String)
    max_medicion = Column(Float)
    min_medicion = Column(Float)
    precision = Column(Float)
    tiempo_respuesta_valor = Column(Integer)
    tiempo_respuesta_unidad = Column(String)
    resolucion = Column(Float)
    temperatura_max = Column(Float)
    temperatura_min = Column(Float)
    voltaje_tipo = Column(String)
    voltaje_min = Column(Float)
    voltaje_max = Column(Float)
    corriente_min = Column(Float)
    corriente_max = Column(Float)
    durabilidad_valor = Column(Integer)
    durabilidad_unidad = Column(String)
    modo_instalacion = Column(String)
    tipo_salida = Column(String)
    certificados = Column(String)
