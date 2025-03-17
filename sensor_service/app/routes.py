from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Sensor
from schemas import SensorCreate, SensorResponse
from uuid import UUID

router = APIRouter()

@router.post("/sensores/", response_model=SensorResponse)
def create_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    """ Crea un sensor sin validar con otros microservicios """
    
    db_sensor = Sensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

@router.get("/sensores/{sensor_id}", response_model=SensorResponse)
def get_sensor(sensor_id: UUID, db: Session = Depends(get_db)):
    """ Obtener un sensor por ID """
    sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    return sensor

@router.get("/sensores/", response_model=list[SensorResponse])
def list_sensores(db: Session = Depends(get_db)):
    """ Listar todos los sensores """
    return db.query(Sensor).all()

@router.put("/sensores/{sensor_id}", response_model=SensorResponse)
def update_sensor(sensor_id: UUID, sensor: SensorCreate, db: Session = Depends(get_db)):
    """ Actualizar un sensor """
    db_sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    
    for key, value in sensor.dict().items():
        setattr(db_sensor, key, value)
    
    db.commit()
    db.refresh(db_sensor)
    return db_sensor

@router.delete("/sensores/{sensor_id}", response_model=SensorResponse)
def delete_sensor(sensor_id: UUID, db: Session = Depends(get_db)):
    """ Eliminar un sensor """
    db_sensor = db.query(Sensor).filter(Sensor.id == sensor_id).first()
    if not db_sensor:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
    
    db.delete(db_sensor)
    db.commit()
    return db_sensor
