from sqlalchemy.orm import Session
from db.models.sensor_node import SensorNode
from db.schemas.sensor_node import SensorNodeCreate

def get_sensor_nodes(db: Session):
    return db.query(SensorNode).all()

def create_sensor_node(db: Session, sensor_node: SensorNodeCreate):
    db_node = SensorNode(**sensor_node.dict())
    db.add(db_node)
    db.commit()
    db.refresh(db_node)
    return db_node
