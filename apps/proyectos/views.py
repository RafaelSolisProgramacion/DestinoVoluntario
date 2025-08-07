from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProyectoForm
from .models import Proyecto
from apps.organizaciones.models import Organizacion

# Create your views here.
def listar_proyectos(request):
    proyectos = Proyecto.objects.all()
    return render(request, 'proyectos/listar_proyectos.html', {'proyectos': proyectos})

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