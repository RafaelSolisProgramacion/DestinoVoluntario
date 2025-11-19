from django import forms
from .models import Postulacion

class PostulacionForm(forms.ModelForm):
    class Meta:
        model = Postulacion
        fields = ['motivation']
        labels = {
            'motivation': 'Motivación'
        }
        widgets = {
            # Hacemos el textarea más grande y con clase de bootstrap para que ocupe todo el ancho
            'motivation': forms.Textarea(attrs={
                'rows': 10,
                'placeholder': '¿Por qué quieres participar en este proyecto?',
                'class': 'form-control',
                'style': 'height:250px;'
            }),
        }
        