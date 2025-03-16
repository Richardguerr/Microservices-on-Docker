import paho.mqtt.client as mqtt
import asyncio

BROKER = "mosquitto"
PORT = 1883
TOPIC = "iot/sensor/data"
USERNAME = "Ricardo"
PASSWORD = "1234"

# Lista para almacenar clientes WebSocket
websocket_clients = []

# Configurar cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.username_pw_set(USERNAME, PASSWORD)

def on_message(client, userdata, message):
    """ Recibe mensajes del broker y los envía a WebSockets """
    data = message.payload.decode()
    print(f"📥 Received MQTT: {data}")

    # Enviar datos a los clientes WebSocket
    for ws in websocket_clients:
        asyncio.run(ws.send_text(data))

mqtt_client.on_message = on_message

async def start_mqtt():
    """ Iniciar la conexión MQTT y suscribirse al topic """
    mqtt_client.connect(BROKER, PORT, 60)
    mqtt_client.subscribe(TOPIC)
    mqtt_client.loop_start()

async def register_websocket(ws):
    """ Agregar WebSocket a la lista y manejar desconexiones """
    websocket_clients.append(ws)
    try:
        while True:
            await asyncio.sleep(1)  # Mantener conexión activa
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        websocket_clients.remove(ws)
