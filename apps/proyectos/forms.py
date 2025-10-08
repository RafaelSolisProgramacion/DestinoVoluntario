from django import forms
from .models import Proyecto

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['title', 'description', 'location', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }