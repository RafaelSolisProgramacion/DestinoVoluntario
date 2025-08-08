from django.urls import path
from . import views

urlpatterns = [
    path('crear/<int:proyecto_id>/', views.crear_postulacion, name='crear_postulacion'),
    path('listar/<int:proyecto_id>/', views.listar_postulaciones, name='listar_postulaciones'),
    path('aprobar/<int:postulacion_id>/', views.aprobar_postulacion, name='aprobar_postulacion'),
    path('rechazar/<int:postulacion_id>/', views.rechazar_postulacion, name='rechazar_postulacion'),
    path('cancelar/<int:postulacion_id>/', views.cancelar_postulacion, name='cancelar_postulacion'),
    path('editar/<int:postulacion_id>/', views.editar_postulacion, name='editar_postulacion'),
    #path('detalle/<int:postulacion_id>/', views.detalle_postulacion, name='detalle_postulacion'),
    #path('mis_postulaciones/', views.mis_postulaciones, name='mis_postulaciones'),
    #path('mis_postulaciones/<int:proyecto_id>/', views.mis_postulaciones_proyecto, name='mis_postulaciones_proyecto'),
    #path('mis_postulaciones/<int:proyecto_id>/detalle/', views.detalle_mis_postulaciones, name='detalle_mis_postulaciones'),
    #path('mis_postulaciones/<int:proyecto_id>/editar/', views.editar_mis_postulaciones, name='editar_mis_postulaciones'),
    #path('mis_postulaciones/<int:proyecto_id>/eliminar/', views.eliminar_mis_postulaciones, name='eliminar_mis_postulaciones'),
]
