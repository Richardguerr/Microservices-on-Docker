from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import SensorNodeService
from db.schemas import SensorNodeCreate, SensorNodeResponse
from db import get_db

router = APIRouter()

@router.post("/", response_model=SensorNodeResponse)
def create_sensor_node(sensor_node: SensorNodeCreate, db: Session = Depends(get_db)):
    """Crea un nuevo nodo sensor."""
    return SensorNodeService.create_sensor_node(sensor_node, db)

@router.get("/", response_model=list[SensorNodeResponse])
def list_sensor_nodes(db: Session = Depends(get_db)):
    """Lista todos los nodos sensores."""
    return SensorNodeService.list_sensor_nodes(db)
