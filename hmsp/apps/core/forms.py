from django import forms
from .models import Suscripcion


class SuscripcionForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Suscripcion.objects.filter(email=email).exists():
            raise forms.ValidationError('El Correo ingresado ya está suscrito.')
        return email

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')
        if not telefono:
            raise forms.ValidationError('El número de teléfono es obligatorio.')
        if len(telefono) != 9:
            raise forms.ValidationError('El número debe tener exactamente 9 dígitos.')
        if not (telefono.startswith('9') or telefono.startswith('2')):
            raise forms.ValidationError('El número debe comenzar con 9 o 2.')
        if not telefono.isdigit():
            raise forms.ValidationError('El número debe contener solo dígitos.')
        return telefono

    class Meta:
        model = Suscripcion
        fields = ['nombre', 'telefono', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+56 | Ej: 912345678',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu correo electrónico',
                'required': True
            })
        }
        labels = {
            'nombre': 'Nombre',
            'telefono': 'Teléfono (+56)',
            'email': 'Correo electrónico'
        }
