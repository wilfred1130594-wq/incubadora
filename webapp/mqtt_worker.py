import paho.mqtt.client as mqtt
import json
from .supabase_client import supabase

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    # Aquí copias la lógica que tenías en tu index.js:
    # Si tipo es "ESTADO", haces el upsert a 'estado_incubadora'
    # Si no, haces el insert a 'datos_incubadora'
    print(f"Datos recibidos: {data}")

client = mqtt.Client()
client.on_message = on_message
client.connect("TU_BROKER_HIVEMQ", 8883)
client.subscribe("jhosimar/rtc")
client.loop_forever()