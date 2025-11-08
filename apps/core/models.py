from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class Usuario(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    # You can add additional fields here if needed
    ROLES = [
        ('voluntario', 'Voluntário'),
        ('organizacion', 'Organización'),
        ('admin', 'Administrador'),
    ]

    role = models.CharField(max_length=20, choices=ROLES, default='voluntario')
    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        related_name='usuarios_grupo',
        blank=True,
        help_text='Grupos a los que pertenece el usuario. Un usuario puede pertenecer a múltiples grupos.',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios_permiso',
        blank=True,
        help_text='Permisos específicos asignados al usuario.',
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
