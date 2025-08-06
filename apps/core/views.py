from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroVoluntarioForm, RegistroOrganizacionForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def registrar_voluntario(request):
    if request.method == 'POST':
        form = RegistroVoluntarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente
            return redirect('dashboard_voluntario')  # Redirigir a la página de inicio del voluntario
            # return HttpResponse("Registro de Voluntario Exitoso")
    else:
        form = RegistroVoluntarioForm()
    return render(request, 'core/registrar_voluntario.html', {'form': form})

def registrar_organizacion(request):
    if request.method == 'POST':
        form = RegistroOrganizacionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente
            return redirect('dashboard_organizacion')  # Redirigir a la página de inicio de la organización
            # return HttpResponse("Registro de Organización Exitoso")
    else:
        form = RegistroOrganizacionForm()
    return render(request, 'core/registrar_organizacion.html', {'form': form})

def home(request):
    return HttpResponse("Bienvenido a Destino Voluntario")

@login_required
def dashboard(request):
    user = request.user
    # Aquí puedes personalizar la lógica para mostrar diferentes dashboards

    if user.role == 'voluntario':
        return render(request, 'core/dashboard_voluntario.html', {'user': user})
        # return HttpResponse("Bienvenido al Dashboard del Voluntario")
    elif user.role == 'organizacion':
        return render(request, 'core/dashboard_organizacion.html', {'user': user})
        # return HttpResponse("Bienvenido al Dashboard de la Organización")
    else:
        return HttpResponse("Bienvenido al Dashboard General")

def logout(request):
    return HttpResponse("Has cerrado sesión exitosamente.")