import paho.mqtt.client as mqtt
import json
import os
import time
from supabase import create_client

# Configuración desde variables de entorno
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
MQTT_BROKER = os.environ.get("MQTT_BROKER")
MQTT_PORT = 8883
MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASS = os.environ.get("MQTT_PASS")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado al broker HiveMQ")
        client.subscribe("jhosimar/rtc")
    else:
        print(f"❌ Fallo en la conexión, código: {rc}")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        print(f"📩 Datos recibidos: {data}")

        # Lógica de procesamiento basada en tu código original
        if data.get("tipo") == "ESTADO":
            supabase.table('estado_incubadora').upsert({
                "id_incubadora": data['id'],
                "estado": data['estado'],
                "set_temp": data['set_temp'],
                "set_hum": data['set_hum'],
                "set_dias": data['set_dias'],
                "set_rot": data['set_rot'],
                "fecha_inicio": data.get('inicio_inc')
            }).execute()
            print("💾 Estado actualizado en Supabase")
        else:
            supabase.table('datos_incubadora').insert({
                "id_incubadora": data['id'],
                "temperatura": data['temp'],
                "humedad": data['hum'],
                "sensor_ok": data.get('sensor_ok', 1)
            }).execute()
            print("💾 Datos registrados en Supabase")

    except Exception as e:
        print(f"❌ Error procesando mensaje: {e}")

# Configuración del Cliente
client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASS)
client.tls_set() # Necesario para conexiones MQTTS (seguras)
client.on_connect = on_connect
client.on_message = on_message

print("⏳ Conectando...")
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Mantener el proceso activo
client.loop_forever()