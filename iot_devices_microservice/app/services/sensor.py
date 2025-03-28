from sqlalchemy.orm import Session
from db.repository import create_sensor, get_sensors
from db.schemas import SensorCreate, SensorResponse

class SensorService:
    @staticmethod
    def create_sensor(sensor_data: SensorCreate, db: Session) -> SensorResponse:
        """Crea un nuevo sensor en la base de datos."""
        return create_sensor(sensor_data, db)

    @staticmethod
    def list_sensors(db: Session) -> list[SensorResponse]:
        """Obtiene todos los sensores registrados en la base de datos."""
        return get_sensors(db)
