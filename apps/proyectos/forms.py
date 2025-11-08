from django import forms
from django.core.exceptions import ValidationError
from .models import Proyecto

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['title', 'description', 'location', 'start_date', 'end_date', 'image']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # Use ClearableFileInput so the clear checkbox appears in edit forms
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput)

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if not image:
            return image

        # Validate file size (max 2MB)
        max_size = 2 * 1024 * 1024  # 2 MB
        if hasattr(image, 'size') and image.size > max_size:
            raise ValidationError('La imagen es demasiado grande (máx. 2 MB).')

        # Validate content type
        valid_mimetypes = ['image/jpeg', 'image/png', 'image/webp']
        content_type = getattr(image, 'content_type', None)
        if content_type and content_type not in valid_mimetypes:
            raise ValidationError('Formato de imagen no soportado. Use JPG, PNG o WEBP.')

        return image