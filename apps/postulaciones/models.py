from django.db import models
from apps.core.models import Usuario
from apps.proyectos.models import Proyecto

# Create your models here.
class Postulacion(models.Model):
    """
    Modelo que representa una postulación a un proyecto de voluntariado.
    """
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    voluntario = models.ForeignKey(Usuario, on_delete=models.CASCADE, limit_choices_to={'role': 'voluntario'})
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    motivation = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voluntario', 'proyecto') # Solo una postulación por voluntario y proyecto
        ordering = ['-applied_at'] # Ordenar por fecha de postulación descendente

    

    def __str__(self):
        return f"Postulación {self.id} - Proyecto {self.proyecto.title} - Voluntario {self.voluntario.username} ({self.status})"