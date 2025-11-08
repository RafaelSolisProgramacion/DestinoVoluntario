from django.urls import path
from .views import listar_proyectos, crear_proyecto, editar_proyecto, cerrar_proyecto, reactivar_proyecto, detalle_proyecto, cancelar_proyecto, buscar_proyectos, eliminar_proyecto
from .views import cambiar_estado_proyecto

urlpatterns = [
    path('listar/', listar_proyectos, name='listar_proyectos'),
    path('buscar/', buscar_proyectos, name='buscar_proyectos'),
    path('crear/', crear_proyecto, name='crear_proyecto'),
    path('editar/<int:proyecto_id>/', editar_proyecto, name='editar_proyecto'),
    path('cerrar/<int:proyecto_id>/', cerrar_proyecto, name='cerrar_proyecto'),
    path('reactivar/<int:proyecto_id>/', reactivar_proyecto, name='reactivar_proyecto'),
    path('detalle/<int:proyecto_id>/', detalle_proyecto, name='detalle_proyecto'),
    path('cancelar/<int:proyecto_id>/', cancelar_proyecto, name='cancelar_proyecto'),
    path('eliminar/<int:proyecto_id>/', eliminar_proyecto, name='eliminar_proyecto'),
    path('cambiar-estado/<int:proyecto_id>/', cambiar_estado_proyecto, name='cambiar_estado_proyecto'),
]
