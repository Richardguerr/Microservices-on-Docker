import asyncio
import json
import random
import uuid
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
import sys

# Configuración MQTT
BROKER = "broker_mosquitto"
PORT = 1883
TOPIC = "iot/sensor/data"
USERNAME = "Ricardo"
PASSWORD = "1234"
QOS = 1  # Calidad de servicio (0, 1 o 2)

# Estructura de datos basada en tus sensores
SENSOR_TYPES = {
    "PM10": {"unit": "µg/m³", "min": 0, "max": 1000},
    "PM2.5": {"unit": "µg/m³", "min": 0, "max": 1000},
    "Temperatura": {"unit": "°C", "min": -50, "max": 50},
    "Humedad": {"unit": "%", "min": 0, "max": 100},
    "Luminosidad": {"unit": "lux", "min": 0, "max": 1000},
    "Ruido": {"unit": "dB", "min": 30, "max": 120},
    "CO2": {"unit": "ppm", "min": 300, "max": 2000},
    "Presión": {"unit": "Pa", "min": 90000, "max": 110000}
}

MANUFACTURERS = ["AirQuality", "HumidTech", "NoiseGuard", "LightMeter", "PressSense", "TempCorp"]
MODELS = ["P3000", "L5000", "N6000", "C4000", "T1000", "H2000"]
INSTALL_TYPES = ["Superficie", "Empotrado", "Colgante"]
PROTOCOLS = ["Digital", "Analógica", "Modbus", "RS485"]
CERTIFICATIONS = ["UL", "CE", "FCC", "ISO 9001", "ISO 14001"]

# Callbacks MQTT
def on_connect(client, userdata, flags, rc, properties=None):
    status = "✅ Conectado" if rc == 0 else f"❌ Error de conexión ({rc})"
    print(f"{status} | Broker: {BROKER}:{PORT} | Topic: {TOPIC}")

def on_disconnect(client, userdata, rc, properties=None):
    if rc != 0:
        print(f"⚠️ Desconexión inesperada (código {rc}). Reconectando...")
        client.reconnect()

def on_publish(client, userdata, mid, reason_code=0, properties=None):
    print(f"📤 Mensaje {mid} publicado (QoS={QOS})", end='\r')

# Configurar cliente MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

# Conectar con manejo de errores
try:
    client.connect(BROKER, PORT, 60)
    client.loop_start()
except Exception as e:
    print(f"❌ Error crítico conectando a MQTT: {e}")
    sys.exit(1)

def generate_sensor_data(node_id):
    """Genera datos de sensor realistas basados en la estructura proporcionada"""
    sensor_type = random.choice(list(SENSOR_TYPES.keys()))
    params = SENSOR_TYPES[sensor_type]
    
    # Generar valor con posible fluctuación
    base_value = random.uniform(params["min"], params["max"] * 0.8)
    current_value = base_value * random.uniform(0.9, 1.1)
    
    return {
        "id": str(uuid.uuid4()),  # UUID único
        "node_id": node_id,
        "type": sensor_type,
        "value": round(current_value, 2),
        "unit": params["unit"],
        "manufacturer": random.choice(MANUFACTURERS),
        "model": random.choice(MODELS),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": random.choice(["OK", "WARNING", "DANGER"]),
        "battery": round(random.uniform(3.0, 4.5)),  # Voltaje típico
        "signal": random.randint(-80, -30),  # dBm
        "installation": random.choice(INSTALL_TYPES),
        "protocols": random.sample(PROTOCOLS, k=random.randint(1, 3)),
        "certifications": random.sample(CERTIFICATIONS, k=random.randint(1, 3)),
        "firmware": f"v{random.randint(1, 3)}.{random.randint(0, 9)}",
        "metadata": {
            "accuracy": round(random.uniform(0.5, 2.5), 2),
            "sampling_rate": f"{random.choice([1, 5, 10, 30])}s",
            "calibration_date": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        }
    }

async def simulate_data():
    """Simula múltiples sensores enviando datos periódicamente"""
    print("🔄 Iniciando simulación de sensores IoT...")
    
    # Crear 34 nodos como en tus datos
    nodes = [f"node_{i}" for i in range(1, 35)]
    
    while True:
        for node_id in nodes:
            data = generate_sensor_data(node_id)
            
            try:
                result = client.publish(
                    TOPIC, 
                    json.dumps(data, ensure_ascii=False), 
                    qos=QOS
                )
                
                # Verificar si se envió correctamente
                if result.rc != mqtt.MQTT_ERR_SUCCESS:
                    print(f"⚠️ Error al publicar (código {result.rc})")
                else:
                    print(f"📡 {node_id} | {data['type']}: {data['value']} {data['unit']} | ", end='\r')
                    
            except Exception as e:
                print(f"❌ Error crítico en publicación: {e}")
                await asyncio.sleep(5)  # Esperar antes de reintentar
            
        await asyncio.sleep(random.uniform(1, 3))  # Variabilidad entre lecturas

async def main():
    """Función principal"""
    try:
        await simulate_data()
    except KeyboardInterrupt:
        print("\n🛑 Deteniendo simulación...")
        client.disconnect()
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())