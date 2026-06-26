import json
import os
import paho.mqtt.publish as publish # 🔹 IMPORTANTE: Esto faltaba
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .supabase_client import supabase

# ... (tus funciones login_view, registro_view, dashboard_view se quedan igual) ...

@csrf_exempt
def actualizar_config_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Solo se permite POST"}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # 🔹 Publicar al ESP32 vía MQTT
        publish.single(
            "jhosimar/config", 
            json.dumps(data), 
            hostname=os.environ.get("MQTT_BROKER"),
            auth={
                'username': os.environ.get("MQTT_USER"), 
                'password': os.environ.get("MQTT_PASS")
            },
            port=8883,
            tls={'ca_certs': None} # A veces es necesario definir el diccionario de tls
        )
        
        return JsonResponse({"status": "ok", "mensaje": "Configuración enviada"})
        
    except Exception as e:
        return JsonResponse({"error": f"Error MQTT: {str(e)}"}, status=500)


def login_view(request):
    return render(request, 'index.html')


def registro_view(request):
    return render(request, 'registro.html')


def dashboard_view(request):
    return render(request, 'dashboard.html')


@csrf_exempt
def login_api(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Método no permitido"},
            status=405
        )

    body = json.loads(request.body)

    usuario = body.get("usuario")
    contrasena = body.get("contrasena")

    respuesta = (
        supabase
        .table("usuarios")
        .select("*")
        .eq("usuario", usuario)
        .eq("contrasena", contrasena)
        .execute()
    )

    if len(respuesta.data) == 0:
        return JsonResponse(
            {"error": "Credenciales inválidas"},
            status=401
        )

    return JsonResponse(respuesta.data[0])

@csrf_exempt
def registro_api(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Método no permitido"},
            status=405
        )

    try:
        body = json.loads(request.body)

        usuario = body.get("usuario")
        contrasena = body.get("contrasena")
        id_incubadora = body.get("id_incubadora")
        celular = body.get("celular")
        email = body.get("email")

        # Verificar incubadora
        incubadora = (
            supabase
            .table("incubadoras")
            .select("id_incubadora")
            .eq("id_incubadora", id_incubadora)
            .execute()
        )

        if len(incubadora.data) == 0:
            return JsonResponse(
                {"error": "La incubadora no existe"},
                status=404
            )

        # Verificar usuario existente
        existe = (
            supabase
            .table("usuarios")
            .select("usuario")
            .eq("usuario", usuario)
            .execute()
        )

        if len(existe.data) > 0:
            return JsonResponse(
                {"error": "Usuario ya registrado"},
                status=400
            )

        # Insertar usuario
        supabase.table("usuarios").insert({
            "usuario": usuario,
            "contrasena": contrasena,
            "id_incubadora": id_incubadora,
            "celular": celular,
            "email": email
        }).execute()

        return JsonResponse({
            "mensaje": "Usuario registrado correctamente"
        })

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )
    

@csrf_exempt
def actualizar_config_api(request):
    if request.method != "POST":
        return JsonResponse({"error": "Solo se permite POST"}, status=405)
    
    try:
        data = json.loads(request.body)
        
        # 🔹 Publicar al ESP32 vía MQTT
        publish.single(
            "jhosimar/config", 
            json.dumps(data), 
            hostname=os.environ.get("MQTT_BROKER"),
            auth={
                'username': os.environ.get("MQTT_USER"), 
                'password': os.environ.get("MQTT_PASS")
            },
            port=8883,
            tls={'ca_certs': None} # A veces es necesario definir el diccionario de tls
        )
        
        return JsonResponse({"status": "ok", "mensaje": "Configuración enviada"})
        
    except Exception as e:
        return JsonResponse({"error": f"Error MQTT: {str(e)}"}, status=500)
@csrf_exempt
def actualizar_config_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        # Publicar al topic de configuración del ESP32
        publish.single(
            "jhosimar/config", 
            json.dumps(data), 
            hostname=os.environ.get("MQTT_BROKER"),
            auth={'username': os.environ.get("MQTT_USER"), 'password': os.environ.get("MQTT_PASS")},
            port=8883,
            tls={'ca_certs': None}
        )
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Método no permitido"}, status=405)

@csrf_exempt
def detener_incubacion_api(request):
    if request.method == "POST":
        # Publicar comando de apagado al ESP32
        data = {
            "estado": "Inactiva",
            "id": id_incubadora # <-- Asegúrate de poner aquí el ID que espera tu ESP32
        }
        publish.single(
            "jhosimar/config", 
            json.dumps(data), 
            hostname=os.environ.get("MQTT_BROKER"),
            auth={'username': os.environ.get("MQTT_USER"), 'password': os.environ.get("MQTT_PASS")},
            port=8883,
            tls={'ca_certs': None}
        )
        return JsonResponse({"status": "ok"})
    return JsonResponse({"error": "Método no permitido"}, status=405)