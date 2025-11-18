from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminPasswordResetForm(PasswordResetForm):
    """Formulario personalizado para recuperación de contraseña de admin"""
    
    def get_users(self, email):
        """Solo permitir recuperación para usuarios staff/superusuarios"""
        active_users = User._default_manager.filter(
            email__iexact=email,
            is_active=True,
            is_staff=True  # Solo usuarios staff pueden recuperar contraseña
        )
        return (
            u for u in active_users
            if u.has_usable_password()
        )
