from django.urls import path
from .views import listar_proyectos, crear_proyecto

urlpatterns = [
    path('listar/', listar_proyectos, name='listar_proyectos'),
    path('crear/', crear_proyecto, name='crear_proyecto'),
]
