from sqlalchemy.orm import Session
from db.models.sensor import Sensor
from db.schemas.sensor import SensorCreate

def get_sensors(db: Session):
    return db.query(Sensor).all()

def create_sensor(db: Session, sensor: SensorCreate):
    db_sensor = Sensor(**sensor.dict())
    db.add(db_sensor)
    db.commit()
    db.refresh(db_sensor)
    return db_sensor
