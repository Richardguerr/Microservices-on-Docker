from fastapi import APIRouter
from app.api.v1.endpoints import sensors, sensor_nodes, iot_gateways

api_router = APIRouter()

api_router.include_router(sensors.router, prefix="/sensors", tags=["Sensores"])
api_router.include_router(sensor_nodes.router, prefix="/sensor-nodes", tags=["Nodos Sensores"])
api_router.include_router(iot_gateways.router, prefix="/iot-gateways", tags=["IoT Gateways"])
