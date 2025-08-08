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