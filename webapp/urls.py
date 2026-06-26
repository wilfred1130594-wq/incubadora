from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view),
    path('registro/', views.registro_view),
    path('dashboard/', views.dashboard_view),

    path('login/', views.login_api),
    path('api/registro/', views.registro_api),
    path('actualizar-config/', views.actualizar_config_api),
    path('actualizar-config/', views.actualizar_config_api, name='actualizar_config'),
    path('detener-incubacion/', views.detener_incubacion_api, name='detener_incubacion'),
]