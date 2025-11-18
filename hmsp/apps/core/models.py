from django.db import models
from django.utils.text import slugify

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
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
    imagen = models.ImageField(upload_to='testimonios/', blank=True, null=True)
    aprobado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-creado']
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
    imagen = models.ImageField(upload_to='noticias/', blank=True, null=True)
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