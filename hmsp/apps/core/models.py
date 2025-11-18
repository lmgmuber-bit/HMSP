from django.db import models
from django.utils.text import slugify

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