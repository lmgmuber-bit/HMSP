from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

class Evento(models.Model):
    TIPO_MULTIMEDIA_CHOICES = [
        ('imagen', 'Imagen'),
        ('video_youtube', 'Video de YouTube'),
        ('video_local', 'Video MP4')
    ]

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.TextField()
    fecha = models.DateTimeField()
    ubicacion = models.CharField(max_length=200, blank=True)
    tipo_multimedia = models.CharField(max_length=20, choices=TIPO_MULTIMEDIA_CHOICES, default='imagen')
    imagen = models.ImageField(upload_to='eventos/', blank=True, null=True)
    video_youtube_url = models.URLField(blank=True, null=True, help_text='Ingresa la URL del video de YouTube')
    video_local = models.FileField(upload_to='eventos/videos/', blank=True, null=True, 
                                help_text='Sube un video en formato MP4',
                                validators=[FileExtensionValidator(allowed_extensions=['mp4'])])
    activo = models.BooleanField(default=True)
    creado = models.DateTimeField(auto_now_add=True)
    modificado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
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