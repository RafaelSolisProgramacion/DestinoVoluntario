from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .forms import PostulacionForm
from .models import Postulacion
from apps.proyectos.models import Proyecto

# Create your views here.
@login_required
def crear_postulacion(request, proyecto_id):
    proyecto = Proyecto.objects.get(id=proyecto_id)
    
    # Verifica si el usuario es un voluntario
    if request.user.role != 'voluntario':
        return redirect('dashboard')
    
    # Verifica si el proyecto existe
    if not proyecto:
        return redirect('dashboard')
    
    # Verifica si el usuario ya ha postulado al proyecto
    if Postulacion.objects.filter(voluntario=request.user, proyecto=proyecto).exists():
        return redirect('dashboard')
    
    # Maneja el formulario de postulación
    if request.method == 'POST':
        form = PostulacionForm(request.POST)
        if form.is_valid():
            postulacion = form.save(commit=False)
            postulacion.voluntario = request.user
            postulacion.proyecto = proyecto
            postulacion.save()
            return redirect('dashboard')  # Redirige al dashboard o a otra página de éxito
    else:
        form = PostulacionForm()
    
    return render(request, 'postulaciones/crear_postulacion.html', {'form': form, 'proyecto': proyecto})

# Mostrar las postulaciones de un proyecto
@login_required
def listar_postulaciones(request, proyecto_id):
    proyecto = Proyecto.objects.get(id=proyecto_id)
    
    # Verifica si el proyecto existe
    if not proyecto:
        return redirect('dashboard')
    
    # Obtiene las postulaciones del proyecto
    postulaciones = Postulacion.objects.filter(proyecto=proyecto)
    
    return render(request, 'postulaciones/listar_postulaciones.html', {'postulaciones': postulaciones, 'proyecto': proyecto})

# Mostrar postulaciones de un voluntario
@login_required
def listar_postulaciones_voluntario(request):
    user = request.user
    if user.role != 'voluntario':
        return redirect('dashboard')

    postulaciones = Postulacion.objects.filter(voluntario=user)
    return render(request, 'postulaciones/listar_postulaciones_voluntario.html', {'postulaciones': postulaciones})

# Aprobar o rechazar una postulación (opcional)
@login_required
def aprobar_postulacion(request, postulacion_id):
    postulacion = Postulacion.objects.get(id=postulacion_id)
    proyecto = postulacion.proyecto
    
    # Verifica si el usuario es una organización
    if request.user.role != 'organizacion':
        return redirect('dashboard')
    
    if request.user.role != 'organizacion' or postulacion.proyecto.organizacion.usuario != request.user:    
        return redirect('dashboard')
    
    postulacion.status = 'aceptada'
    postulacion.save()
    return redirect('listar_postulaciones', proyecto_id=proyecto.id)

@login_required
def rechazar_postulacion(request, postulacion_id):
    postulacion = Postulacion.objects.get(id=postulacion_id)
    proyecto = postulacion.proyecto
    
    # Verifica si el usuario es una organización
    if request.user.role != 'organizacion':
        return redirect('dashboard')
    
    if request.user.role != 'organizacion' or postulacion.proyecto.organizacion.usuario != request.user:    
        return redirect('dashboard')
    
    postulacion.status = 'rechazada'
    postulacion.save()
    return redirect('listar_postulaciones', proyecto_id=proyecto.id)

# Cancelar una postulación (opcional)
@login_required
def cancelar_postulacion(request, postulacion_id):
    postulacion = Postulacion.objects.get(id=postulacion_id)
    proyecto = postulacion.proyecto
    
    # Verifica si el usuario es un voluntario
    if request.user.role != 'voluntario':
        return redirect('dashboard')
    
    if postulacion.voluntario != request.user:
        return redirect('dashboard')
    
    postulacion.delete()
    # Redirige a la lista de postulaciones del voluntario
    return redirect('listar_postulaciones_voluntario')

# Editar una postulación (opcional)
@login_required
def editar_postulacion(request, postulacion_id):
    postulacion = Postulacion.objects.get(id=postulacion_id)
    proyecto = postulacion.proyecto
    
    # Verifica si el usuario es un voluntario
    if request.user.role != 'voluntario':
        return redirect('dashboard')
    
    if postulacion.voluntario != request.user:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PostulacionForm(request.POST, instance=postulacion)
        if form.is_valid():
            form.save()
            # Redirige a la lista de postulaciones del voluntario
            return redirect('listar_postulaciones_voluntario')
    else:
        form = PostulacionForm(instance=postulacion)
    
    return render(request, 'postulaciones/editar_postulacion.html', {'form': form, 'proyecto': proyecto})