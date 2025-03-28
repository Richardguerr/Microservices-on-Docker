from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from services import IoTGatewayService
from db.schemas import IoTGatewayCreate, IoTGatewayResponse
from db import get_db

router = APIRouter()

@router.post("/", response_model=IoTGatewayResponse)
def create_iot_gateway(gateway: IoTGatewayCreate, db: Session = Depends(get_db)):
    """Crea un nuevo IoT Gateway."""
    return IoTGatewayService.create_iot_gateway(gateway, db)

@router.get("/", response_model=list[IoTGatewayResponse])
def list_iot_gateways(db: Session = Depends(get_db)):
    """Lista todos los IoT Gateways."""
    return IoTGatewayService.list_iot_gateways(db)
