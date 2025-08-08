from django import forms
from .models import Postulacion

class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['motivation']
        widgets = {
            'motivation': forms.Textarea(attrs={'rows': 4, 'placeholder': '¿Por qué quieres participar en este proyecto?'}),
        }
        