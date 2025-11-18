from django.core.management.base import BaseCommand
from django.utils import timezone
from hmsp.apps.core.models import Evento, Testimonio, Oracion, Noticia
from datetime import timedelta

class Command(BaseCommand):
    help = 'Crea datos de ejemplo para el sitio'

    def handle(self, *args, **kwargs):
        # Eventos de ejemplo
        eventos = [
            {
                'titulo': 'Retiro Espiritual de Primavera',
                'descripcion': 'Un fin de semana de renovación espiritual y conexión con Dios. Incluye meditaciones, oraciones y momentos de reflexión personal.',
                'fecha': timezone.now() + timedelta(days=7),
                'ubicacion': 'Casa de Retiros Santa María',
                'activo': True
            },
            {
                'titulo': 'Jornada de Oración por la Paz',
                'descripcion': 'Unidos en oración por la paz mundial. Una jornada especial de intercesión y adoración.',
                'fecha': timezone.now() + timedelta(days=14),
                'ubicacion': 'Santuario Nacional',
                'activo': True
            },
            {
                'titulo': 'Encuentro Juvenil Misionero',
                'descripcion': 'Jóvenes unidos en la misión. Actividades, talleres y momentos de oración para descubrir tu vocación misionera.',
                'fecha': timezone.now() + timedelta(days=21),
                'ubicacion': 'Centro Pastoral Juvenil',
                'activo': True
            },
            {
                'titulo': 'Celebración del Día de Santa Teresa',
                'descripcion': 'Celebración especial en honor a Santa Teresa. Misa solemne, procesión y compartir comunitario.',
                'fecha': timezone.now() + timedelta(days=28),
                'ubicacion': 'Capilla Santa Teresa',
                'activo': True
            },
            {
                'titulo': 'Taller de Formación Misionera',
                'descripcion': 'Formación intensiva para nuevos misioneros. Aprenderemos sobre evangelización, pastoral y trabajo comunitario.',
                'fecha': timezone.now() + timedelta(days=35),
                'ubicacion': 'Centro de Formación Misionera',
                'activo': True
            },
            {
                'titulo': 'Rosario por las Vocaciones',
                'descripcion': 'Jornada de oración especial por las vocaciones religiosas y misioneras. Rosario meditado y adoración.',
                'fecha': timezone.now() + timedelta(days=42),
                'ubicacion': 'Santuario Mariano',
                'activo': True
            }
        ]

        for evento_data in eventos:
            event = Evento(**evento_data)
            event.save()  # This will handle the slug creation
            self.stdout.write(f'Creado evento: {evento_data["titulo"]}')

        # Testimonios de ejemplo
        testimonios = [
            {
                'nombre': 'María González',
                'testimonio': 'Mi vida cambió completamente después del retiro espiritual. Encontré paz y un nuevo propósito en mi caminar con Dios.',
                'aprobado': True
            },
            {
                'nombre': 'Juan Pérez',
                'testimonio': 'Las hermanas misioneras me ayudaron a redescubrir mi fe en momentos difíciles. Su apoyo y oraciones fueron fundamentales.',
                'aprobado': True
            }
        ]

        for testimonio_data in testimonios:
            Testimonio.objects.create(**testimonio_data)
            self.stdout.write(f'Creado testimonio de: {testimonio_data["nombre"]}')

        # Oraciones de ejemplo
        oraciones = [
            {
                'titulo': 'Oración por la Paz Interior',
                'contenido': 'Señor, concédeme la serenidad para aceptar las cosas que no puedo cambiar, el valor para cambiar las que puedo y la sabiduría para reconocer la diferencia.',
                'categoria': 'Personal',
                'activa': True
            },
            {
                'titulo': 'Oración por las Familias',
                'contenido': 'Padre celestial, bendice y protege a todas las familias. Que encuentren en ti la fuente del amor y la unidad.',
                'categoria': 'Familia',
                'activa': True
            },
            {
                'titulo': 'Oración por los Enfermos',
                'contenido': 'Señor Jesús, médico divino, extiende tu mano sanadora sobre todos los que sufren enfermedades. Concédeles tu paz y consuelo.',
                'categoria': 'Sanación',
                'activa': True
            }
        ]

        for oracion_data in oraciones:
            Oracion.objects.create(**oracion_data)
            self.stdout.write(f'Creada oración: {oracion_data["titulo"]}')

        # Noticias de ejemplo
        noticias = [
            {
                'titulo': 'Nueva Casa de Oración Inaugurada',
                'contenido': 'Con gran alegría anunciamos la apertura de una nueva casa de oración que servirá como centro de encuentro y espiritualidad para nuestra comunidad.',
                'creado': timezone.now() - timedelta(days=2),
                'destacada': True
            },
            {
                'titulo': 'Exitosa Misión en Comunidades Rurales',
                'contenido': 'Las hermanas misioneras completaron una exitosa misión de tres meses en comunidades rurales, llevando esperanza y apoyo espiritual.',
                'creado': timezone.now() - timedelta(days=5),
                'destacada': True
            },
            {
                'titulo': 'Programa de Formación Espiritual',
                'contenido': 'Iniciamos un nuevo programa de formación espiritual para laicos comprometidos. Las inscripciones están abiertas.',
                'creado': timezone.now() - timedelta(days=7),
                'destacada': True
            },
            {
                'titulo': 'Bendición de Nueva Capilla en Comunidad Rural',
                'contenido': 'Con gran gozo compartimos la bendición de una nueva capilla en la comunidad de San José. Este espacio sagrado será un faro de esperanza y fe para los habitantes de la zona.',
                'creado': timezone.now() - timedelta(days=9),
                'destacada': True
            },
            {
                'titulo': 'Encuentro Internacional de Jóvenes Misioneros',
                'contenido': 'Más de 100 jóvenes de diferentes países se reunieron para compartir experiencias y fortalecer su compromiso misionero. El evento incluyó talleres, oraciones y proyectos comunitarios.',
                'creado': timezone.now() - timedelta(days=12),
                'destacada': True
            },
            {
                'titulo': 'Celebración del Aniversario de la Congregación',
                'contenido': 'Con inmensa gratitud celebramos un año más de servicio y dedicación. La santa misa fue presidida por el obispo diocesano, seguida de un emotivo homenaje a las hermanas pioneras.',
                'creado': timezone.now() - timedelta(days=15),
                'destacada': True
            }
        ]

        for noticia_data in noticias:
            noticia = Noticia(**noticia_data)
            noticia.save()  # This will handle the slug creation
            self.stdout.write(f'Creada noticia: {noticia_data["titulo"]}')