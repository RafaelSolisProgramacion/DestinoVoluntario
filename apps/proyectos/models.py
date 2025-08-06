from django.db import models
from apps.organizaciones.models import Organizacion

# Create your models here.
class Proyecto(models.Model):
    """
    Modelo que representa un proyecto de voluntariado.
    """
    ESTADOS = [
        ('activo', 'Activo'),
        ('cerrado', 'Cerrado'),
        ('evaluacion', 'En Evaluación'),
    ]

    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=ESTADOS, default='activo')

    def __str__(self):
        return f"{self.title} {self.organizacion.name} ({self.status})"