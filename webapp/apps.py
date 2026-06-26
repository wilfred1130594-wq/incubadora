from django.apps import AppConfig
import threading
import os

class WebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'webapp'

    def ready(self):
        # Evita que el worker se ejecute dos veces en el entorno de desarrollo de Django
        if os.environ.get('RUN_MAIN', None) != 'true':
            from .mqtt_worker import iniciar_mqtt_en_hilo
            
            # Iniciamos el worker en un hilo separado para no bloquear el servidor web
            worker_thread = threading.Thread(target=iniciar_mqtt_en_hilo, daemon=True)
            worker_thread.start()
            
            print("🚀 Worker MQTT iniciado en segundo plano")