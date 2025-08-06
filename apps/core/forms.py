from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario
from apps.organizaciones.models import Organizacion

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
    nombre = forms.CharField(max_length=255, required=True)
    descripcion = forms.CharField(widget=forms.Textarea)
    website = forms.URLField(required=False)

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'organizacion'  # Asignar el rol de organizacion
        if commit:
            user.save()
            # Crear una instancia de Organizacion asociada al usuario
            Organizacion.objects.create(
                usuario=user,
                name=self.cleaned_data['nombre'],
                description=self.cleaned_data['descripcion'],
                website=self.cleaned_data['website']
            )
        return user