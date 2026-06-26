from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

from .supabase_client import supabase


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
    if request.method == "POST":
        # 1. Recibes el JSON del frontend
        # 2. Publicas el mensaje al broker MQTT (usando la librería paho-mqtt)
        # 3. Retornas {"status": "ok"}
        return JsonResponse({"status": "ok"})