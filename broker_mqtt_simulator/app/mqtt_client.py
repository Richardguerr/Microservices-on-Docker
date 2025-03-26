import paho.mqtt.client as mqtt
import asyncio
from threading import Thread

BROKER = "mosquitto"
PORT = 1883
TOPIC = "iot/sensor/data"
USERNAME = "Ricardo"
PASSWORD = "1234"

websocket_clients = set()  # Conjunto de clientes WebSocket conectados
message_queue = asyncio.Queue()
main_loop = None  # Variable para guardar referencia al bucle principal

# Usar la versión 2 de la API
mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.username_pw_set(USERNAME, PASSWORD)

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"✅ Conectado al broker MQTT con código: {rc}")
    # Suscribirse al topic cuando se conecta
    client.subscribe(TOPIC)
    print(f"✅ Suscrito al topic: {TOPIC}")

def on_message(client, userdata, message):
    """ Maneja los mensajes recibidos desde MQTT. """
    data = message.payload.decode()
    print(f"📥 MQTT Recibido: {data}")
    
    # Usar la referencia global al bucle principal
    if main_loop is not None:
        main_loop.call_soon_threadsafe(lambda: asyncio.ensure_future(message_queue.put(data), loop=main_loop))
    else:
        print("❌ Error: No hay un bucle de eventos disponible")

async def process_messages():
    """ Enviar mensajes desde MQTT a WebSockets. """
    while True:
        data = await message_queue.get()
        print(f"📤 Enviando a WebSockets: {data}")

        disconnected_clients = set()
        for ws in websocket_clients:
            try:
                await ws.send_text(data)
            except Exception as e:
                print(f"❌ Error WebSocket: {e}")
                disconnected_clients.add(ws)

        websocket_clients.difference_update(disconnected_clients)  # 🔹 Elimina clientes desconectados

async def start_mqtt():
    """ Conectar a MQTT y suscribirse al tópico. """
    global main_loop
    main_loop = asyncio.get_running_loop()  # Guardar referencia al bucle principal
    
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connect
    
    # Iniciar MQTT en un hilo separado
    def start_mqtt_loop():
        try:
            mqtt_client.connect(BROKER, PORT, 60)
            mqtt_client.loop_forever()
        except Exception as e:
            print(f"❌ Error en el bucle MQTT: {e}")
    
    # Crear y ejecutar el hilo MQTT
    mqtt_thread = Thread(target=start_mqtt_loop)
    mqtt_thread.daemon = True  # El hilo terminará cuando termine el programa principal
    mqtt_thread.start()

async def register_websocket(ws):
    """ Registra un WebSocket y envía datos de prueba. """
    await ws.accept()
    websocket_clients.add(ws)
    print("✅ WebSocket conectado.")

    try:
        while True:
            msg = await ws.receive_text()
            print(f"📩 Mensaje recibido del WebSocket: {msg}")
    except Exception:
        pass  # 🔹 Evita imprimir errores de desconexión
    finally:
        websocket_clients.discard(ws)
        print("🔌 WebSocket eliminado.")