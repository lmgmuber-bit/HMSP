import os
import json
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hmsp.settings')
django.setup()

from django.core import serializers
from django.contrib.auth.models import User
from hmsp.apps.core.models import Evento, Noticia, Testimonio

def export_model_data(model, filename):
    data = serializers.serialize('json', model.objects.all(), indent=2)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)
    print(f"Exported {model.__name__} data to {filename}")
    # Verificar el contenido del archivo
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"First few characters of {filename}: {content[:50]}")

# Exportar usuarios
export_model_data(User, 'auth_user_clean.json')

# Exportar modelos de core
export_model_data(Evento, 'eventos_clean.json')
export_model_data(Noticia, 'noticias_clean.json')
export_model_data(Testimonio, 'testimonios_clean.json')