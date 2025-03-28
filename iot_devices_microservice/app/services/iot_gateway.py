from sqlalchemy.orm import Session
from db.repository import create_iot_gateway, get_iot_gateways
from db.schemas import IoTGatewayCreate, IoTGatewayResponse

class IoTGatewayService:
    @staticmethod
    def create_iot_gateway(gateway_data: IoTGatewayCreate, db: Session) -> IoTGatewayResponse:
        """Crea un nuevo IoT Gateway en la base de datos."""
        return create_iot_gateway(gateway_data, db)

    @staticmethod
    def list_iot_gateways(db: Session) -> list[IoTGatewayResponse]:
        """Obtiene todos los IoT Gateways registrados."""
        return get_iot_gateways(db)
