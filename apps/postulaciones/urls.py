from django.urls import path
from . import views

urlpatterns = [
    path('crear/<int:proyecto_id>/', views.crear_postulacion, name='crear_postulacion'),
    path('listar/<int:proyecto_id>/', views.listar_postulaciones, name='listar_postulaciones'),
]
