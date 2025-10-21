import asyncio
import json
import random
import uuid
from sensors_config import CERTIFICATIONS, INSTALL_TYPES, MANUFACTURERS, PROTOCOLS, SENSOR_TYPES
import paho.mqtt.client as mqtt
from datetime import datetime, timedelta
import sys
from collections import defaultdict

# Importar el servicio de email y configuración
from email_service import EmailNotificationService
from config_email import EMAIL_CONFIG, ALERT_RECIPIENTS, ALERT_SETTINGS, validate_config

# Configuración MQTT
BROKER = "broker_mosquitto"
PORT = 1883
TOPIC = "iot/sensor/data"
USERNAME = "Ricardo"
PASSWORD = "1234"
QOS = 1  # Calidad de servicio (0, 1 o 2)


class SensorState:
    """Mantiene el estado de cada sensor para generar datos realistas"""
    def __init__(self, sensor_type, params):
        self.sensor_type = sensor_type
        self.params = params
        self.current_value = random.uniform(*params["typical_range"])
        self.last_update = datetime.utcnow()
        self.trend = random.choice(["stable", "increasing", "decreasing"])
        self.anomaly_chance = 0.03  # 3% chance de anomalía
        
    def update_value(self):
        """Actualiza el valor del sensor con tendencias realistas"""
        # Cambiar tendencia ocasionalmente
        if random.random() < 0.1:
            self.trend = random.choice(["stable", "increasing", "decreasing"])
        
        # Calcular cambio basado en tendencia
        typical_min, typical_max = self.params["typical_range"]
        change_rate = (typical_max - typical_min) * 0.05  # 5% de cambio máximo
        
        if self.trend == "increasing":
            change = random.uniform(0, change_rate)
        elif self.trend == "decreasing":
            change = random.uniform(-change_rate, 0)
        else:  # stable
            change = random.uniform(-change_rate * 0.3, change_rate * 0.3)
        
        # Aplicar cambio con ruido
        noise = random.gauss(0, change_rate * 0.1)
        self.current_value += change + noise
        
        # Anomalía ocasional
        if random.random() < self.anomaly_chance:
            # Spike temporal
            spike = random.uniform(change_rate * 2, change_rate * 5)
            self.current_value += spike if random.random() > 0.5 else -spike
        
        # Mantener dentro de límites físicos
        self.current_value = max(self.params["min"], 
                                min(self.params["max"], self.current_value))
        
        self.last_update = datetime.utcnow()
        return round(self.current_value, 2)
    
    def get_status(self):
        """Determina el estado basado en umbrales de seguridad"""
        value = self.current_value
        params = self.params
        
        # Para oxígeno, la lógica es inversa (menor es peor)
        if self.sensor_type == "O2":
            if value < params.get("danger_threshold", 0):
                return "DANGER"
            elif value < params.get("warning_threshold", 0):
                return "WARNING"
            elif params.get("safe_min", 0) <= value <= params.get("safe_max", 100):
                return "OK"
            else:
                return "WARNING"
        
        # Para parámetros con límites superior e inferior (humedad, iluminación, pH)
        if self.sensor_type in ["Humedad", "Iluminación", "pH_Agua"]:
            safe_min = params.get("safe_min", 0)
            safe_max = params.get("safe_max", 100)
            
            if value < safe_min or value > params.get("danger_threshold", safe_max):
                return "DANGER"
            elif value < params.get("warning_threshold_low", safe_min) or value > params.get("warning_threshold_high", safe_max):
                return "WARNING"
            else:
                return "OK"
        
        # Para el resto de sensores (gases, partículas, ruido, etc.)
        if value >= params.get("danger_threshold", float('inf')):
            return "DANGER"
        elif value >= params.get("warning_threshold", float('inf')):
            return "WARNING"
        else:
            return "OK"

# Diccionario para mantener el estado de cada sensor
sensor_states = {}

# Variables globales para emails
email_service = None
alert_cooldowns = defaultdict(lambda: datetime.min)
email_stats = defaultdict(int)

# Callbacks MQTT
def on_connect(client, userdata, flags, rc, properties=None):
    status = "✅ Conectado" if rc == 0 else f"❌ Error de conexión ({rc})"
    print(f"{status} | Broker: {BROKER}:{PORT} | Topic: {TOPIC}")
    print(f"📋 Simulando {len(SENSOR_TYPES)} tipos de sensores conforme a ISO 45001/14001 y DS 024-2016-EM")

def on_disconnect(client, userdata, rc, properties=None):
    if rc != 0:
        print(f"⚠️ Desconexión inesperada (código {rc}). Reconectando...")
        client.reconnect()

def on_publish(client, userdata, mid, reason_code=0, properties=None):
    pass  # Evitar spam en consola

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

def get_sensor_state(node_id, sensor_type):
    """Obtiene o crea el estado de un sensor"""
    key = f"{node_id}_{sensor_type}"
    if key not in sensor_states:
        sensor_states[key] = SensorState(sensor_type, SENSOR_TYPES[sensor_type])
    return sensor_states[key]

def should_send_alert(sensor_key, status):
    """Determina si se debe enviar una alerta según cooldown"""
    if status == "OK":
        return False
    
    now = datetime.now()
    last_alert = alert_cooldowns[sensor_key]
    cooldown = timedelta(minutes=ALERT_SETTINGS["cooldown_minutes"])
    
    if now - last_alert > cooldown:
        alert_cooldowns[sensor_key] = now
        return True
    return False

async def send_email_alert(data):
    """Envía alerta por email si corresponde"""
    global email_stats
    email_service = EmailNotificationService(**EMAIL_CONFIG)

    status = data["status"]
    sensor_type = data["type"]
    sensor_key = f"{data['node_id']}_{sensor_type}"
    
    # Verificar si debe enviar
    if not should_send_alert(sensor_key, status):
        return
    
    # Obtener destinatarios
    recipients = ALERT_RECIPIENTS.get(status, [])
    if not recipients:
        return
    
    print(f"\n{'🔴' if status == 'DANGER' else '🟡'} Enviando alerta por email...")
    print(f"   Sensor: {sensor_type} | Estado: {status}")
    print(f"   Destinatarios: {len(recipients)}")
    
    # Enviar email
    success = email_service.send_alert(recipients, data, status)
    
    if success:
        email_stats["sent"] += 1
        email_stats[status.lower()] += 1
        print(f"   ✅ Email enviado correctamente")
    else:
        email_stats["failed"] += 1
        print(f"   ❌ Error al enviar email")

def generate_sensor_data(node_id):
    """Genera datos de sensor realistas basados en normas ISO y DS 024-2016-EM"""
    sensor_type = random.choice(list(SENSOR_TYPES.keys()))
    params = SENSOR_TYPES[sensor_type]
    
    # Obtener estado del sensor
    state = get_sensor_state(node_id, sensor_type)
    current_value = state.update_value()
    status = state.get_status()
    
    # Seleccionar fabricante y modelo
    manufacturer = random.choice(list(MANUFACTURERS.keys()))
    model = random.choice(MANUFACTURERS[manufacturer])
    
    # Última calibración (debe ser < 1 año según ISO 9001)
    last_calibration = datetime.now() - timedelta(days=random.randint(0, 350))
    next_calibration = last_calibration + timedelta(days=365)
    
    return {
        "id": str(uuid.uuid4()),
        "node_id": node_id,
        "type": sensor_type,
        "description": f"Sensor de {sensor_type}",
        "value": current_value,
        "unit": params["unit"],
        "status": status,
        "manufacturer": manufacturer,
        "model": model,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "battery": round(random.uniform(3.2, 4.2), 2) if random.random() > 0.3 else None,
        "signal_strength": random.randint(-85, -40),  # dBm
        "installation_type": random.choice(INSTALL_TYPES),
        "communication_protocol": random.choice(PROTOCOLS),
        "certifications": random.sample(CERTIFICATIONS, k=random.randint(2, 4)),
        "firmware_version": f"v{random.randint(1, 3)}.{random.randint(0, 12)}.{random.randint(0, 5)}",
        "safety_thresholds": {
            "safe_max": params.get("safe_max"),
            "safe_min": params.get("safe_min"),
            "warning": params.get("warning_threshold"),
            "danger": params.get("danger_threshold")
        },
        "metadata": {
            "accuracy": f"±{round(random.uniform(0.5, 3.0), 2)}%",
            "sampling_rate": f"{random.choice([1, 2, 5, 10, 30, 60])}s",
            "response_time": f"{random.choice([1, 2, 5, 10])}s",
            "last_calibration": last_calibration.strftime("%Y-%m-%d"),
            "next_calibration": next_calibration.strftime("%Y-%m-%d"),
            "calibration_status": "Valid" if (next_calibration > datetime.now()) else "Expired",
            "operating_temp": f"-10 to 50 °C",
            "ip_rating": random.choice(["IP65", "IP67", "IP68"]),
            "compliance": ["ISO 45001", "ISO 14001", "DS 024-2016-EM"]
        },
            "location": {
            "zone": random.choice([
                "Mina Principal Subterránea", 
                "Zona de Túneles Norte", 
                "Área de Procesamiento", 
                "Sector de Extracción A"
            ]),
            "sector": random.choice([
                "Producción", 
                "Ventilación", 
                "Transporte", 
                "Mantenimiento", 
                "Seguridad",
                "Extracción",
                "Procesamiento",
                "Almacenamiento"
            ]),
            "coordinates": {
                "x": round(random.uniform(-1000, 1000), 2),
                "y": round(random.uniform(-1000, 1000), 2),
                "z": round(random.uniform(-500, 0), 2)  # Profundidad
            }
        }
    }

async def simulate_data():
    """Simula múltiples sensores enviando datos periódicamente"""
    print("🔄 Iniciando simulación de sensores IoT con reglas ISO...\n")
    
    nodes = [f"node_{i:03d}" for i in range(1, 35)]
    message_count = 0
    danger_count = 0
    warning_count = 0
    
    while True:
        for node_id in nodes:
            data = generate_sensor_data(node_id)
            message_count += 1
            
            # Contadores de estado
            if data["status"] == "DANGER":
                danger_count += 1
            elif data["status"] == "WARNING":
                warning_count += 1
            
            try:
                result = client.publish(
                    TOPIC, 
                    json.dumps(data, ensure_ascii=False, indent=2), 
                    qos=QOS
                )
                
                if result.rc == mqtt.MQTT_ERR_SUCCESS:
                 
                    # ENVIAR CORREO SI ES ALERTA
                  """   if data["status"] in ["DANGER", "WARNING"]:
                       await send_email_alert(data)
                          """
                else:
                    print(f"\nError al publicar (código {result.rc})")
                    
            except Exception as e:
                print(f"\nError crítico en publicación: {e}")
                await asyncio.sleep(5)
        
    
            
        await asyncio.sleep(random.uniform(2, 4))

