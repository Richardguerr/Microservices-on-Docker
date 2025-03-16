from fastapi import FastAPI, WebSocket
import asyncio
from mqtt_client import start_mqtt, register_websocket
from simulator import simulate_data

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "IoT Gateway is running"}

# Iniciar el cliente MQTT en segundo plano

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """ Endpoint WebSocket para transmitir datos en tiempo real. """
    await websocket.accept()
    await register_websocket(websocket)


@app.on_event("startup")
async def start_simulation():
    asyncio.create_task(start_mqtt())
    asyncio.create_task(simulate_data())  # 🔹 Ejecuta el simulador en segundo plano
