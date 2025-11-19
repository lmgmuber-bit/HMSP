#!/usr/bin/env python
"""
Script para poblar las secciones de Recursos con datos de ejemplo
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hmsp.settings')
django.setup()

from hmsp.apps.core.models import ConfiguracionSitio

# Obtener la configuración del sitio
config = ConfiguracionSitio.get_configuracion()

# Recursos - Información General
config.recursos_titulo = 'Recursos Espirituales'
config.recursos_contenido = '''Bienvenidos a nuestra sección de recursos espirituales. Aquí encontrarás herramientas y materiales para fortalecer tu vida de fe y tu camino espiritual.

Explora nuestras colecciones de oraciones, materiales de formación, boletines informativos y opciones para colaborar con nuestra misión. Cada recurso ha sido preparado con amor y dedicación para acompañarte en tu crecimiento espiritual.'''

# Biblioteca de Oraciones
config.biblioteca_oraciones_titulo = 'Biblioteca de Oraciones'
config.biblioteca_oraciones_contenido = '''Nuestra biblioteca de oraciones ofrece una amplia colección de rezos y devociones para acompañarte en tu vida espiritual diaria. Desde oraciones tradicionales hasta meditaciones contemplativas, encontrarás recursos para fortalecer tu relación con Dios.

Incluyendo:
- Oraciones del Santo Rosario
- Liturgia de las Horas
- Devociones marianas
- Oraciones por intenciones especiales
- Meditaciones guiadas
- Novenas y triduos

Cada oración es una puerta que se abre al encuentro con el Señor.'''

# Material Espiritual
config.material_espiritual_titulo = 'Material Espiritual'
config.material_espiritual_contenido = '''Accede a una selección de materiales de formación espiritual cuidadosamente elaborados por nuestra comunidad. Estos recursos están diseñados para profundizar en la fe católica y enriquecer tu caminar espiritual.

Nuestros materiales incluyen:
- Catequesis y formación bíblica
- Reflexiones sobre los sacramentos
- Enseñanzas de los santos
- Documentos del Magisterio
- Guías para la oración contemplativa
- Retiros espirituales en audio y video

"La Palabra de Dios es viva y eficaz" (Hebreos 4:12)'''

# Boletín Mensual
config.boletin_mensual_titulo = 'Boletín Mensual'
config.boletin_mensual_contenido = '''Suscríbete a nuestro boletín mensual "Palabra Viva" y mantente conectado con las actividades, reflexiones y noticias de nuestra comunidad.

Cada mes compartimos:
- Calendario de eventos y retiros
- Reflexiones del mes litúrgico
- Testimonios de fe
- Recursos espirituales recomendados
- Actividades de la comunidad
- Intenciones de oración

Recibe inspiración y acompañamiento directo en tu correo electrónico. ¡Únete a nuestra familia espiritual!'''

# Donaciones
config.donaciones_titulo = 'Donaciones'
config.donaciones_contenido = '''Tu generosidad hace posible nuestra misión de servir a Dios y a la comunidad. Las donaciones nos ayudan a:

- Mantener nuestras actividades pastorales
- Organizar retiros y encuentros espirituales
- Apoyar obras de caridad y misión
- Formar nuevas vocaciones
- Mantener nuestros espacios de oración
- Producir materiales de formación

Cada aporte, grande o pequeño, es una bendición que nos permite continuar siendo instrumentos del Señor. Si deseas colaborar con nuestra misión, contáctanos para conocer las diferentes formas de donación.

"Cada uno dé según lo que haya decidido en su corazón, no de mala gana ni por obligación, porque Dios ama al que da con alegría." (2 Corintios 9:7)'''

# Guardar los cambios
config.save()

print('✓ Contenido de ejemplo agregado exitosamente a todas las secciones de Recursos:')
print(f'  - {config.recursos_titulo}')
print(f'  - {config.biblioteca_oraciones_titulo}')
print(f'  - {config.material_espiritual_titulo}')
print(f'  - {config.boletin_mensual_titulo}')
print(f'  - {config.donaciones_titulo}')
print('\n¡Listo! Ahora puedes ver la página /recursos/ con todo el contenido.')
