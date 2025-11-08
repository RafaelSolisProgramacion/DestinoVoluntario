from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Proyecto

@login_required
@require_POST
def cambiar_estado_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    if request.user.role == 'organizacion':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in ['activo', 'inactivo']:
            proyecto.status = nuevo_estado
            proyecto.save()
    return redirect(request.META.get('HTTP_REFERER', 'listar_proyectos'))
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProyectoForm
from .models import Proyecto
from apps.organizaciones.models import Organizacion
from apps.postulaciones.models import Postulacion
from django.db.models import Q

# Create your views here.
def listar_proyectos(request):
    proyectos = Proyecto.objects.all()
    organizaciones = Organizacion.objects.all()
    user = request.user
    postulaciones = Postulacion.objects.all()

    # Filtro por organización
    organizacion_id = request.GET.get('organizacion')
    if organizacion_id and organizacion_id != 'todas':
        proyectos = proyectos.filter(organizacion_id=organizacion_id)

    # Filtro por estado
    estado = request.GET.get('estado')
    if estado:
        proyectos = proyectos.filter(status=estado)

    # Ordenar
    ordenar = request.GET.get('ordenar', 'fecha-inicio')
    if ordenar == 'fecha-inicio':
        proyectos = proyectos.order_by('start_date')
    elif ordenar == 'fecha-fin':
        proyectos = proyectos.order_by('end_date')

    return render(request, 'proyectos/listado_proyectos.html', 
                  {
                      'proyectos': proyectos, 
                      'user': user, 
                      'postulaciones': postulaciones,
                      'organizaciones': organizaciones
                  })

# Ver detalles del proyecto.
def detalle_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    user = request.user
    postulaciones = Postulacion.objects.filter(proyecto=proyecto)

    # Voluntarios aceptados
    voluntarios_aceptados = Postulacion.objects.filter(proyecto=proyecto, status='aceptada').count()
    postulantes_aceptados = Postulacion.objects.filter(proyecto=proyecto, status='aceptada').values_list('voluntario__email', flat=True)

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
        'postulaciones_pendientes': postulaciones_pendientes,
        'postulantes_aceptados': postulantes_aceptados
    }

    return render(request, 'proyectos/detalle_proyecto.html', context)

@login_required
def crear_proyecto(request):
    user = request.user

    # Verificamos que el usuario sea una organizacion
    if user.role != 'organizacion':
        return redirect('dashboard')

    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
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
        form = ProyectoForm(request.POST, request.FILES, instance=proyecto)
        if form.is_valid():
            # Handle clearable file input: if the clear checkbox is checked, Django will set image to False
            proyecto = form.save(commit=False)
            # If image was cleared via ClearableFileInput, cleaned_data['image'] may be False
            if 'image-clear' in request.POST and request.POST.get('image-clear'):
                proyecto.image = None
            proyecto.save()
            return redirect('dashboard')  # Redirigir al dashboard de la organización
    else:
        form = ProyectoForm(instance=proyecto)
    return render(request, 'proyectos/editar_proyecto.html', {'form': form, 'proyecto': proyecto})

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


# Eliminar proyecto
@login_required
@require_POST
def eliminar_proyecto(request, proyecto_id):
    user = request.user
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)

    # Solo la organización dueña puede eliminar
    if user.role != 'organizacion' or proyecto.organizacion != user.organizacion:
        return redirect('dashboard')

    # Borrar y redirigir al dashboard
    proyecto.delete()
    return redirect('dashboard')

def buscar_proyectos(request):
    query = request.GET.get('q', '')
    proyectos = Proyecto.objects.all()
    if query:
        proyectos = proyectos.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    user = request.user
    return render(
        request, 
        'proyectos/buscar_proyectos.html', 
        {
            'proyectos': proyectos, 
            'query': query, 
            'user': user
        }
    )