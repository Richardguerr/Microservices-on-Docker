from pydantic import BaseModel, UUID4
from typing import Optional

class SensorCreate(BaseModel):
    id_node: str
    variable: str
    marca: str
    referencia: str
    unidad_medicion: Optional[str]
    max_medicion: Optional[float]
    min_medicion: Optional[float]
    precision: Optional[float]
    tiempo_respuesta_valor: Optional[int]
    tiempo_respuesta_unidad: Optional[str]
    resolucion: Optional[float]
    temperatura_max: Optional[float]
    temperatura_min: Optional[float]
    voltaje_tipo: Optional[str]
    voltaje_min: Optional[float]
    voltaje_max: Optional[float]
    corriente_min: Optional[float]
    corriente_max: Optional[float]
    durabilidad_valor: Optional[int]
    durabilidad_unidad: Optional[str]
    modo_instalacion: Optional[str]
    tipo_salida: Optional[str]
    certificados: Optional[str]

class SensorResponse(SensorCreate):
    id: UUID4

    class Config:
        from_attributes = True
