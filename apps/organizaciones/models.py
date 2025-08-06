from django.db import models
from apps.core.models import Usuario

# Create your models here.
class Organizacion(models.Model):
    """
    Modelo que representa una organizacion.
    """
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE,)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name