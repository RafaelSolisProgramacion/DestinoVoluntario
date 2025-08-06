from django.db import models
from django.contrib.auth.models import AbstractUser

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

    def __str__(self):
        return f"{self.username} ({self.role})"
