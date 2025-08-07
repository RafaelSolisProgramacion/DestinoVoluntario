from django.urls import path
from .views import listar_proyectos, crear_proyecto, editar_proyecto

urlpatterns = [
    path('listar/', listar_proyectos, name='listar_proyectos'),
    path('crear/', crear_proyecto, name='crear_proyecto'),
    path('editar/<int:proyecto_id>/', editar_proyecto, name='editar_proyecto'),
]
