from sqlalchemy.orm import Session
from db.models.iot_gateway import IoTGateway
from db.schemas.iot_gateway import IoTGatewayCreate

def get_iot_gateways(db: Session):
    return db.query(IoTGateway).all()

def create_iot_gateway(db: Session, gateway: IoTGatewayCreate):
    db_gateway = IoTGateway(**gateway.dict())
    db.add(db_gateway)
    db.commit()
    db.refresh(db_gateway)
    return db_gateway
