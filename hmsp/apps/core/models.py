
from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

# Modelo para suscripciones de usuarios

class Suscripcion(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9, blank=False, help_text="Número chileno, 9 dígitos, inicia con 9 o 2")
    email = models.EmailField(unique=True)
    fecha_suscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} <{self.email}>"

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(
        upload_to='eventos/',
        blank=True,
        null=True,
        help_text='ESPECIFICACIONES: Dimensiones: 1200x800 píxeles (relación 3:2) para carrusel principal, '
                  'o 600x400 píxeles para vista de lista. '
                  'Formato: JPG (preferido) o PNG. '
                  'Tamaño máximo: 2MB. '
                  'La imagen se optimizará automáticamente para web.'
    )
    orden_carrusel = models.IntegerField(
        default=0,
        help_text='Orden en el carrusel (1-5 para mostrar, 0 para no mostrar). Los eventos con 0 aparecerán en próximos eventos.'
    )
    fecha_inicio_publicacion = models.DateTimeField(
        null=True, 
        blank=True,
        help_text='Fecha desde la que el evento será visible. Si está vacío, el evento será visible inmediatamente.'
    )
    fecha_fin_publicacion = models.DateTimeField(
        null=True, 
        blank=True,
        help_text='Fecha hasta la que el evento será visible. Si está vacío, el evento será visible indefinidamente.'
    )
    tipo_multimedia = models.CharField(max_length=20, choices=[
        ('ninguno', 'Ninguno'),
        ('video_youtube', 'Video de YouTube'),
        ('video_local', 'Video Local')
    ], default='ninguno')
    video_youtube_url = models.URLField(blank=True, null=True)
    video_local = models.FileField(upload_to='eventos/videos/', blank=True, null=True)
    preferencia_visualizacion = models.CharField(max_length=20, choices=[
        ('imagen', 'Mostrar Imagen'),
        ('video', 'Mostrar Video')
    ], default='imagen', help_text='Seleccione qué mostrar en el carrusel cuando el evento tenga tanto imagen como video')
    formulario_url = models.URLField(blank=True, null=True, verbose_name='URL Formulario Google')
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    def get_youtube_embed_url(self):
        """Convierte URL de YouTube a formato embed con modo de privacidad mejorada"""
        if not self.video_youtube_url:
            return None
        
        # Extraer el ID del video de diferentes formatos de URL
        import re
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&?\s]+)',  # youtube.com/watch?v= o youtu.be/
            r'youtube\.com\/embed\/([^?&\s]+)',  # ya está en formato embed
            r'youtube-nocookie\.com\/embed\/([^?&\s]+)',  # formato nocookie
        ]
        
        for pattern in patterns:
            match = re.search(pattern, self.video_youtube_url)
            if match:
                video_id = match.group(1)
                # Limpiar cualquier parámetro adicional del video_id
                video_id = video_id.split('?')[0].split('&')[0]
                # Usar dominio youtube-nocookie.com para evitar restricciones
                return f'https://www.youtube-nocookie.com/embed/{video_id}'
        
        return self.video_youtube_url  # Si no coincide, devolver original

    class Meta:
        ordering = ['orden_carrusel', '-fecha']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        
        # Verificar estado de publicación según fechas
        from django.utils import timezone
        now = timezone.now()
        
        # Por defecto, asumimos que está activo si no hay cambio explícito
        if not hasattr(self, '_explicit_active'):
            # Si tiene fecha de fin y ya pasó, desactivar
            if self.fecha_fin_publicacion and self.fecha_fin_publicacion < now:
                self.activo = False
                self.orden_carrusel = 0  # Limpiar orden del carrusel
            # Si tiene fecha de inicio y aún no llega, desactivar
            elif self.fecha_inicio_publicacion and self.fecha_inicio_publicacion > now:
                self.activo = False
                self.orden_carrusel = 0  # Limpiar orden del carrusel
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class Testimonio(models.Model):
    nombre = models.CharField(max_length=100)
    testimonio = models.TextField()
    imagen = models.ImageField(
        upload_to='testimonios/',
        blank=True,
        null=True,
        help_text='ESPECIFICACIONES: Dimensiones: 400x400 píxeles (cuadrada, 1:1). '
                  'Formato: JPG (preferido) o PNG. '
                  'Tamaño máximo: 500KB. '
                  'Usar foto de rostro centrada con buena iluminación.'
    )
    aprobado = models.BooleanField(default=False)
    destacado = models.BooleanField(
        default=False,
        help_text='Marcar para mostrar en la página principal. Solo los primeros 3 testimonios destacados se mostrarán.'
    )
    orden_destacado = models.IntegerField(
        default=0,
        help_text='Orden de visualización en la página principal (1, 2 o 3). Use 0 para no destacar.'
    )
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['orden_destacado', '-creado']
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'

    def __str__(self):
        return f"Testimonio de {self.nombre}"

class Oracion(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    categoria = models.CharField(max_length=50, choices=[
        ('Personal', 'Personal'),
        ('Familia', 'Familia'),
        ('Sanacion', 'Sanación'),
        ('Intercesion', 'Intercesión'),
    ])
    activa = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['categoria', 'titulo']
        verbose_name = 'Oración'
        verbose_name_plural = 'Oraciones'

    def __str__(self):
        return f"{self.categoria} - {self.titulo}"

class Noticia(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    contenido = models.TextField()
    imagen = models.ImageField(
        upload_to='noticias/',
        blank=True,
        null=True,
        help_text='ESPECIFICACIONES: Dimensiones: 800x600 píxeles (relación 4:3) para portada, '
                  'o 400x300 píxeles para miniatura. '
                  'Formato: JPG (preferido) o PNG. '
                  'Tamaño máximo: 1.5MB. '
                  'Usar imágenes de alta calidad y bien iluminadas.'
    )
    destacada = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado']
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class ConfiguracionSitio(models.Model):
    """Modelo para gestionar la configuración general del sitio"""
    # Logo
    logo_principal = models.ImageField(
        upload_to='configuracion/',
        blank=True,
        null=True,
        help_text='ESPECIFICACIONES DEL LOGO: Dimensiones recomendadas: 200x80 píxeles (máximo 300x120). '
                  'Formato: PNG con fondo transparente (preferido) o JPG. '
                  'Tamaño máximo: 500KB. '
                  'El logo se mostrará con altura de 60px en la navegación.'
    )
    
    # Quiénes Somos
    quienes_somos_titulo = models.CharField(
        max_length=200,
        default='Quiénes Somos',
        verbose_name='Título de Quiénes Somos'
    )
    quienes_somos_contenido = models.TextField(
        blank=True,
        verbose_name='Contenido de Quiénes Somos',
        help_text='Describe quién es HMSP y su misión'
    )
    quienes_somos_imagen = models.ImageField(
        upload_to='configuracion/',
        blank=True,
        null=True,
        verbose_name='Imagen de Quiénes Somos',
        help_text='Dimensiones recomendadas: 1200x600 píxeles. Formato: JPG o PNG. Tamaño máximo: 2MB.'
    )
    
    # Historia
    historia_titulo = models.CharField(
        max_length=200,
        default='Nuestra Historia',
        verbose_name='Título de Historia'
    )
    historia_contenido = models.TextField(
        blank=True,
        verbose_name='Contenido de Historia',
        help_text='Cuenta la historia de HMSP'
    )
    historia_imagen = models.ImageField(
        upload_to='configuracion/',
        blank=True,
        null=True,
        verbose_name='Imagen de Historia',
        help_text='Dimensiones recomendadas: 800x500 píxeles. Formato: JPG o PNG. Tamaño máximo: 1.5MB.'
    )
    
    # Vocaciones
    vocaciones_titulo = models.CharField(
        max_length=200,
        default='Vocaciones',
        verbose_name='Título de Vocaciones'
    )
    vocaciones_contenido = models.TextField(
        blank=True,
        verbose_name='Contenido de Vocaciones',
        help_text='Información sobre vocaciones y llamados'
    )
    vocaciones_imagen = models.ImageField(
        upload_to='configuracion/',
        blank=True,
        null=True,
        verbose_name='Imagen de Vocaciones',
        help_text='Dimensiones recomendadas: 800x500 píxeles. Formato: JPG o PNG. Tamaño máximo: 1.5MB.'
    )
    
    # Recursos
    recursos_titulo = models.CharField(
        max_length=200,
        default='Recursos',
        verbose_name='Título de Recursos'
    )
    recursos_contenido = models.TextField(
        blank=True,
        verbose_name='Contenido de Recursos',
        help_text='Información general sobre los recursos disponibles'
    )
    recursos_imagen = models.ImageField(
        upload_to='configuracion/',
        blank=True,
        null=True,
        verbose_name='Imagen de Recursos',
        help_text='Dimensiones recomendadas: 1200x600 píxeles. Formato: JPG o PNG. Tamaño máximo: 2MB.'
    )
    
    # Biblioteca de Oraciones
    biblioteca_oraciones_titulo = models.CharField(
        max_length=200,
        default='Biblioteca de Oraciones',
        verbose_name='Título de Biblioteca de Oraciones'
    )
    biblioteca_oraciones_contenido = models.TextField(
        blank=True,
        verbose_name='Contenido de Biblioteca de Oraciones',
        help_text='Descripción de la colección de oraciones disponibles'
    )
    biblioteca_oraciones_imagen = models.ImageField(
        upload_to='configuracion/',
        blank=True,
        null=True,
        verbose_name='Imagen de Biblioteca de Oraciones',
        help_text='Dimensiones recomendadas: 800x500 píxeles. Formato: JPG o PNG. Tamaño máximo: 1.5MB.'
    )
    
    # Material Espiritual
    material_espiritual_titulo = models.CharField(
        max_length=200,
        default='Material Espiritual',
        verbose_name='Título de Material Espiritual'
    )
    material_espiritual_contenido = models.TextField(
        blank=True,
        verbose_name='Contenido de Material Espiritual',
        help_text='Información sobre material de formación espiritual'
    )
    material_espiritual_imagen = models.ImageField(
        upload_to='configuracion/',
        blank=True,
        null=True,
        verbose_name='Imagen de Material Espiritual',
        help_text='Dimensiones recomendadas: 800x500 píxeles. Formato: JPG o PNG. Tamaño máximo: 1.5MB.'
    )
    
    # Boletín Mensual
    boletin_mensual_titulo = models.CharField(
        max_length=200,
        default='Boletín Mensual',
        verbose_name='Título de Boletín Mensual'
    )
    boletin_mensual_contenido = models.TextField(
        blank=True,
        verbose_name='Contenido de Boletín Mensual',
        help_text='Descripción del boletín y cómo suscribirse'
    )
    boletin_mensual_imagen = models.ImageField(
        upload_to='configuracion/',
        blank=True,
        null=True,
        verbose_name='Imagen de Boletín Mensual',
        help_text='Dimensiones recomendadas: 800x500 píxeles. Formato: JPG o PNG. Tamaño máximo: 1.5MB.'
    )
    
    # Donaciones
    donaciones_titulo = models.CharField(
        max_length=200,
        default='Donaciones',
        verbose_name='Título de Donaciones'
    )
    donaciones_contenido = models.TextField(
        blank=True,
        verbose_name='Contenido de Donaciones',
        help_text='Información sobre cómo realizar donaciones'
    )
    donaciones_imagen = models.ImageField(
        upload_to='configuracion/',
        blank=True,
        null=True,
        verbose_name='Imagen de Donaciones',
        help_text='Dimensiones recomendadas: 800x500 píxeles. Formato: JPG o PNG. Tamaño máximo: 1.5MB.'
    )
    
    # Información de Contacto
    contacto_direccion = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Dirección'
    )
    contacto_telefono = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Teléfono'
    )
    contacto_email = models.EmailField(
        blank=True,
        verbose_name='Correo Electrónico'
    )
    contacto_horario = models.TextField(
        blank=True,
        verbose_name='Horario de Atención',
        help_text='Horarios de atención al público'
    )
    
    # Redes Sociales
    facebook_url = models.URLField(blank=True, verbose_name='Facebook')
    instagram_url = models.URLField(blank=True, verbose_name='Instagram')
    youtube_url = models.URLField(blank=True, verbose_name='YouTube')
    twitter_url = models.URLField(blank=True, verbose_name='Twitter/X')
    
    # Metadatos
    actualizado = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuración del Sitio'
        verbose_name_plural = 'Configuración del Sitio'
    
    def save(self, *args, **kwargs):
        # Asegurar que solo exista una instancia
        if not self.pk and ConfiguracionSitio.objects.exists():
            # Si ya existe una configuración, actualizar esa en lugar de crear una nueva
            configuracion = ConfiguracionSitio.objects.first()
            self.pk = configuracion.pk
        super().save(*args, **kwargs)
    
    def __str__(self):
        return 'Configuración del Sitio'
    
    @classmethod
    def get_configuracion(cls):
        """Obtener o crear la configuración del sitio"""
        configuracion, created = cls.objects.get_or_create(pk=1)
        return configuracion

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=200, verbose_name='Nombre')
    email = models.EmailField(verbose_name='Correo Electrónico')
    asunto = models.CharField(max_length=200, verbose_name='Asunto')
    mensaje = models.TextField(verbose_name='Mensaje')
    leido = models.BooleanField(default=False, verbose_name='Leído')
    respondido = models.BooleanField(default=False, verbose_name='Respondido')
    creado = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Envío')
    
    class Meta:
        ordering = ['-creado']
        verbose_name = 'Mensaje de Contacto'
        verbose_name_plural = 'Mensajes de Contacto'
    
    def __str__(self):
        return f"{self.nombre} - {self.asunto} ({self.creado.strftime('%d/%m/%Y')})"


class Apostolado(models.Model):
    titulo = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(unique=True, blank=True)
    descripcion_corta = models.TextField(max_length=300, verbose_name='Descripción Corta', help_text='Breve descripción para el menú')
    descripcion = models.TextField(verbose_name='Descripción Completa')
    imagen = models.ImageField(
        upload_to='apostolados/',
        blank=True,
        null=True,
        verbose_name='Imagen',
        help_text='ESPECIFICACIONES: Dimensiones: 800x600px (recomendado). Formato: JPG, PNG, SVG. Máx 2MB.'
    )
    orden = models.IntegerField(default=0, verbose_name='Orden', help_text='Orden de aparición en el menú (menor número = primero)')
    activo = models.BooleanField(default=True, verbose_name='Activo')
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['orden', 'titulo']
        verbose_name = 'Apostolado'
        verbose_name_plural = 'Apostolados'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo