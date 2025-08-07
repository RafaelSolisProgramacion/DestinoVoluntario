from django.shortcuts import render, redirect
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
            return redirect('listar_proyectos')
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/crear_proyecto.html', {'form': form})
