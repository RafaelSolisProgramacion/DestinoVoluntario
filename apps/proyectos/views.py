from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProyectoForm
from .models import Proyecto
from apps.organizaciones.models import Organizacion
from apps.postulaciones.models import Postulacion

# Create your views here.
def listar_proyectos(request):
    proyectos = Proyecto.objects.all()
    user = request.user
    postulaciones = Postulacion.objects.all()
    return render(request, 'proyectos/listar_proyectos.html', {'proyectos': proyectos, 'user': user, 'postulaciones': postulaciones})

# Ver detalles del proyecto.
def detalle_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    user = request.user
    postulaciones = Postulacion.objects.filter(proyecto=proyecto)
    
    # Voluntarios aceptados
    voluntarios_aceptados = Postulacion.objects.filter(proyecto=proyecto, status='aceptada').count()

    # Postulacion usuario actual
    postulacion_usuario = None
    if user.is_authenticated and user.role == 'voluntario':
        postulacion_usuario = Postulacion.objects.filter(proyecto=proyecto, voluntario=user).first()
    
    # Postulaciones pendientes (si es organizacion)
    postulaciones_pendientes = []
    if user.is_authenticated and user.role == 'organizacion':
        if proyecto.organizacion.usuario == user:
            postulaciones_pendientes = postulaciones.filter(status='pendiente')

    context = {
        'proyecto': proyecto,
        'user': user,
        'postulaciones': postulaciones,
        'voluntarios_aceptados': voluntarios_aceptados,
        'postulacion_usuario': postulacion_usuario,
        'postulaciones_pendientes': postulaciones_pendientes
    }

    return render(request, 'proyectos/detalle_proyecto.html', context)

@login_required
def crear_proyecto(request):
    user = request.user

    # Verificamos que el usuario sea una organizacion
    if user.role != 'organizacion':
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            proyecto = form.save(commit=False)
            proyecto.organizacion = user.organizacion
            proyecto.save()
            return redirect('dashboard')  # Redirigir al dashboard de la organización
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/crear_proyecto.html', {'form': form})

@login_required
def editar_proyecto(request, proyecto_id):
    user = request.user
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    # Verificamos que el usuario sea la organizacion dueña del proyecto
    if user.role != 'organizacion' or proyecto.organizacion != user.organizacion:
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirigir al dashboard de la organización
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'proyectos/editar_proyecto.html', {'form': form})

@login_required
def cerrar_proyecto(request, proyecto_id):
    user = request.user
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    # Verificamos que el usuario sea la organizacion dueña del proyecto
    if user.role != 'organizacion' or proyecto.organizacion != user.organizacion:
        return redirect('dashboard')

    if request.method == 'POST':
        proyecto.status = 'cerrado'
        proyecto.save()
        return redirect('dashboard')  # Redirigir al dashboard de la organización
    return render(request, 'proyectos/editar_proyecto.html', {'proyecto': proyecto})

@login_required
def reactivar_proyecto(request, proyecto_id):
    user = request.user
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    # Verificamos que el usuario sea la organizacion dueña del proyecto
    if user.role != 'organizacion' or proyecto.organizacion != user.organizacion:
        return redirect('dashboard')

    if request.method == 'POST':
        proyecto.status = 'activo'
        proyecto.save()
        return redirect('dashboard')  # Redirigir al dashboard de la organización
    return render(request, 'proyectos/editar_proyecto.html', {'proyecto': proyecto})

# Cancelar proyecto
@login_required
def cancelar_proyecto(request, proyecto_id):
    user = request.user
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    # Verificamos que el usuario sea la organizacion dueña del proyecto
    if user.role != 'organizacion' or proyecto.organizacion != user.organizacion:
        return redirect('dashboard')

    if request.method == 'POST':
        confirmar = request.POST.get('confirmar_cancelacion')
        if confirmar == 'yes':
            proyecto.status = 'cancelado'
            proyecto.save()
            return redirect('dashboard')  # Redirigir al dashboard de la organización
        else:
            return render(request, 'proyectos/cancelar_proyecto.html', {
                'proyecto': proyecto,
                'error': 'Debes confirmar la cancelacion marcando la casilla.'
                })
    return render(request, 'proyectos/cancelar_proyecto.html', {'proyecto': proyecto})
