import json
import os
import paho.mqtt.publish as publish
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .supabase_client import supabase

# --- Vistas de páginas ---
def login_view(request): return render(request, 'index.html')
def registro_view(request): return render(request, 'registro.html')
def dashboard_view(request): return render(request, 'dashboard.html')

# --- APIs de autenticación ---
@csrf_exempt
def login_api(request):
    if request.method != "POST": return JsonResponse({"error": "Método no permitido"}, status=405)
    body = json.loads(request.body)
    respuesta = supabase.table("usuarios").select("*").eq("usuario", body.get("usuario")).eq("contrasena", body.get("contrasena")).execute()
    if len(respuesta.data) == 0: return JsonResponse({"error": "Credenciales inválidas"}, status=401)
    return JsonResponse(respuesta.data[0])

@csrf_exempt
def registro_api(request):
    if request.method != "POST": return JsonResponse({"error": "Método no permitido"}, status=405)
    try:
        body = json.loads(request.body)
        # ... (Tu lógica de registro existente)
        supabase.table("usuarios").insert({"usuario": body.get("usuario"), "contrasena": body.get("contrasena"), "id_incubadora": body.get("id_incubadora"), "celular": body.get("celular"), "email": body.get("email")}).execute()
        return JsonResponse({"mensaje": "Usuario registrado correctamente"})
    except Exception as e: return JsonResponse({"error": str(e)}, status=500)

# --- APIs de control MQTT ---
@csrf_exempt
def actualizar_config_api(request):
    if request.method != "POST": return JsonResponse({"error": "Solo POST"}, status=405)
    try:
        data = json.loads(request.body)
        publish.single(
            "jhosimar/config", json.dumps(data),
            hostname=os.environ.get("MQTT_BROKER"),
            auth={'username': os.environ.get("MQTT_USER"), 'password': os.environ.get("MQTT_PASS")},
            port=8883, tls={'ca_certs': None}
        )
        return JsonResponse({"status": "ok"})
    except Exception as e: return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def detener_incubacion_api(request):
    if request.method != "POST": return JsonResponse({"error": "Solo POST"}, status=405)
    try:
        body = json.loads(request.body)
        data = {"estado": "Inactiva", "id": body.get("id")}
        publish.single(
            "jhosimar/config", json.dumps(data),
            hostname=os.environ.get("MQTT_BROKER"),
            auth={'username': os.environ.get("MQTT_USER"), 'password': os.environ.get("MQTT_PASS")},
            port=8883, tls={'ca_certs': None}
        )
        return JsonResponse({"status": "ok"})
    except Exception as e: return JsonResponse({"error": str(e)}, status=500)