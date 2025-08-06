from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario

# Para Voluntario
class RegistroVoluntarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'voluntario'  # Asignar el rol de voluntario
        if commit:
            user.save()
        return user
    
# Para Organizacion
class RegistroOrganizacionForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'organizacion'  # Asignar el rol de organizacion
        if commit:
            user.save()
        return user