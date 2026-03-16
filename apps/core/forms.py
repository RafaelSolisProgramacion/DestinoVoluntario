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

# Formulario de login por username o email
from django.contrib.auth import authenticate
class UsernameOrEmailLoginForm(forms.Form):
    identifier = forms.CharField(label="Usuario o correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def clean(self):
        identifier = self.cleaned_data.get('identifier')
        password = self.cleaned_data.get('password')
        user = None
        if identifier and password:
            # Buscar por email
            try:
                user_obj = Usuario.objects.get(email=identifier)
                user = authenticate(username=user_obj.username, password=password)
            except Usuario.DoesNotExist:
                # Buscar por username
                user = authenticate(username=identifier, password=password)
            if user is None:
                raise forms.ValidationError("Usuario/correo o contraseña incorrectos.")
            self.user = user
        return self.cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)

# Formulario de login por email
class EmailLoginForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            try:
                user = Usuario.objects.get(email=email)
            except Usuario.DoesNotExist:
                raise forms.ValidationError("Correo o contraseña incorrectos.")
            user = authenticate(username=user.username, password=password)
            if user is None:
                raise forms.ValidationError("Correo o contraseña incorrectos.")
            self.user = user
        return self.cleaned_data

    def get_user(self):
        return getattr(self, 'user', None)
    
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