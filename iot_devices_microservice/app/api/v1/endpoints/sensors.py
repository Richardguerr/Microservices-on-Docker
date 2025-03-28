from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import SensorService
from db.schemas import SensorCreate, SensorResponse
from db import get_db

router = APIRouter()

@router.post("/", response_model=SensorResponse)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    """Crea un nuevo sensor."""
    return SensorService.create_sensor(sensor, db)

@router.get("/", response_model=list[SensorResponse])
def list_sensors(db: Session = Depends(get_db)):
    """Lista todos los sensores."""
    return SensorService.list_sensors(db)
