import asyncio
import json
import random
import paho.mqtt.client as mqtt

BROKER = "mosquitto"
PORT = 1883
TOPIC = "iot/sensor/data"
USERNAME = "Ricardo"
PASSWORD = "1234"

client = mqtt.Client()
client.username_pw_set(USERNAME, PASSWORD)
client.connect(BROKER, PORT, 60)
client.loop_start()

async def simulate_data():
    while True:
        data = {
            "sensor_id": random.randint(1, 10),
            "temperature": round(random.uniform(20.0, 30.0), 2),
            "humidity": round(random.uniform(40.0, 60.0), 2)
        }
        client.publish(TOPIC, json.dumps(data))
        print(f"Published: {data}")
        await asyncio.sleep(2)  # 🔹 Usar await para que no bloquee
