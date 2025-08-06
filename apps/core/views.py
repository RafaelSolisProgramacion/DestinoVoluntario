from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroVoluntarioForm, RegistroOrganizacionForm
from django.http import HttpResponse

# Create your views here.
def registrar_voluntario(request):
    if request.method == 'POST':
        form = RegistroVoluntarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente
            # return redirect('dashboard_voluntario')  # Redirigir a la página de inicio del voluntario
            return HttpResponse("Registro de Voluntario Exitoso")
    else:
        form = RegistroVoluntarioForm()
    return render(request, 'core/registrar_voluntario.html', {'form': form})

def registrar_organizacion(request):
    if request.method == 'POST':
        form = RegistroOrganizacionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente
            # return redirect('dashboard_organizacion')  # Redirigir a la página de inicio de la organización
            return HttpResponse("Registro de Organización Exitoso")
    else:
        form = RegistroOrganizacionForm()
    return render(request, 'core/registrar_organizacion.html', {'form': form})

def home(request):
    return HttpResponse("Bienvenido a Destino Voluntario")