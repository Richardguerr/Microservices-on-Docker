from sqlalchemy.orm import Session
from db.repository import create_sensor_node, get_sensor_nodes
from db.schemas import SensorNodeCreate, SensorNodeResponse

class SensorNodeService:
    @staticmethod
    def create_sensor_node(node_data: SensorNodeCreate, db: Session) -> SensorNodeResponse:
        """Crea un nuevo nodo sensor en la base de datos."""
        return create_sensor_node(node_data, db)

    @staticmethod
    def list_sensor_nodes(db: Session) -> list[SensorNodeResponse]:
        """Obtiene todos los nodos sensores registrados."""
        return get_sensor_nodes(db)
