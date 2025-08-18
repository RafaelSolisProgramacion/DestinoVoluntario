from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroVoluntarioForm, RegistroOrganizacionForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from apps.proyectos.models import Proyecto
from apps.organizaciones.models import Organizacion
from apps.postulaciones.models import Postulacion
from django.core.paginator import Paginator

# Create your views here.
def registrar_voluntario(request):
    if request.user.is_authenticated:
        return redirect('home')  
    
    if request.method == 'POST':
        form = RegistroVoluntarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente
            return redirect('dashboard')  # Redirigir a la página de inicio del voluntario
            # return HttpResponse("Registro de Voluntario Exitoso")
    else:
        form = RegistroVoluntarioForm()
    return render(request, 'core/registrar_voluntario.html', {'form': form})

def registrar_organizacion(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistroOrganizacionForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Iniciar sesión automáticamente
            return redirect('dashboard')  # Redirigir a la página de inicio de la organización
            # return HttpResponse("Registro de Organización Exitoso")
    else:
        form = RegistroOrganizacionForm()
    return render(request, 'core/registrar_organizacion.html', {'form': form})

def home(request):
    # return HttpResponse("Bienvenido a Destino Voluntario")
    proyectos = Proyecto.objects.all()
    paginate_by = 9  # Número de proyectos por página
    page_number = request.GET.get('page', 1)
    paginator = Paginator(proyectos, paginate_by)
    page_obj = paginator.get_page(page_number)

    if request.htmx:
        return render(
            request, 
            'proyectos/listar_proyectos.html', 
            {
                'proyectos': page_obj,
                'user': request.user,
                'pagination_url': request.path  # URL para la paginación
            }
        )
    else:
        return render(request, 'core/index.html', {'proyectos': page_obj})

@login_required
def dashboard(request):
    user = request.user
    paginate_by = 6
    page_number = request.GET.get('page', 1)
    # Aquí puedes personalizar la lógica para mostrar diferentes dashboards

    if user.role == 'voluntario':
        proyectos = Proyecto.objects.all()
        postulaciones = Postulacion.objects.filter(voluntario=user)
        proyectos_postulados = set(postulaciones.values_list('proyecto_id', flat=True))
        postulaciones_por_proyecto = {
            p.proyecto_id: p for p in postulaciones
        }
        paginator = Paginator(proyectos, paginate_by)
        page_obj = paginator.get_page(page_number)

        if request.htmx:
            return render(
                request, 
                'proyectos/listar_proyectos.html', 
                {
                    'proyectos': page_obj,
                    'user': user,
                    'postulados': proyectos_postulados,
                    'postulaciones_por_proyecto': postulaciones_por_proyecto,
                    'pagination_url': request.path  # URL para la paginación
                }
            )
        else:
            return render(
                request, 
                'core/dashboard_voluntario.html', 
                {
                 'user': user, 
                 'proyectos': page_obj, 
                 'postulados': proyectos_postulados, 
                 'postulaciones_por_proyecto': postulaciones_por_proyecto
                 }
            )
        # return HttpResponse("Bienvenido al Dashboard del Voluntario")
    elif user.role == 'organizacion':
        organizacion = Organizacion.objects.get(usuario=user)
        proyectos = Proyecto.objects.filter(organizacion=organizacion)
        paginator = Paginator(proyectos, paginate_by)
        page_obj = paginator.get_page(page_number)

        if request.htmx:
            return render(
                request, 
                'proyectos/listar_proyectos.html', 
                {
                    'proyectos': page_obj, 
                    'user': user,
                    'pagination_url': request.path  # URL para la paginación
                }
            )
        else:
            return render(
                request, 
                'core/dashboard_organizacion.html', 
                {
                    'user': user, 
                    'proyectos': page_obj
                }
            )
        # return HttpResponse("Bienvenido al Dashboard de la Organización")
    else:
        return HttpResponse("Bienvenido al Dashboard General")

def logout(request):
    return HttpResponse("Has cerrado sesión exitosamente.")