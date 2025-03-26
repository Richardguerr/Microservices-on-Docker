import asyncio
import json
import random
import paho.mqtt.client as mqtt

BROKER = "mosquitto"
PORT = 1883
TOPIC = "iot/sensor/data"
USERNAME = "Ricardo"
PASSWORD = "1234"

# Callbacks para monitorear conexión
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"✅ Conectado al broker con resultado: {rc}")

def on_disconnect(client, userdata, rc, properties=None):
    print(f"❌ Desconectado del broker con código: {rc}")
    
# Corregir la firma de la función on_publish para VERSION2
def on_publish(client, userdata, mid, reason_code=0, properties=None):
    print(f"✅ Mensaje {mid} publicado correctamente")

# Configuración del cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

# Conectar con manejo de errores
try:
    client.connect(BROKER, PORT, 60)
    client.loop_start()  # Mantiene MQTT funcionando en un hilo aparte
except Exception as e:
    print(f"❌ Error conectando a MQTT: {e}")

async def simulate_data():
    """ Simula el envío de datos cada 2 segundos """
    print("🔄 Iniciando simulación de datos...")
    while True:
        data = {
            "sensor_id": random.randint(1, 10),
            "temperature": round(random.uniform(20.0, 30.0), 2),
            "humidity": round(random.uniform(40.0, 60.0), 2)
        }
        
        # Publicar en MQTT
        try:
            client.publish(TOPIC, json.dumps(data), qos=1)  # Usar QoS 1 para garantizar entrega
            print(f"📤 Datos enviados: {data}")
        except Exception as e:
            print(f"⚠️ Error publicando: {e}")
        
        # Forzar flush de stdout para evitar buffering
        import sys
        sys.stdout.flush()
        
        await asyncio.sleep(2)  # No bloquea el event loop

async def main():
    """ Ejecuta la simulación de datos """
    await simulate_data()

# Ejecutar el loop de asyncio
if __name__ == "__main__":
    asyncio.run(main())