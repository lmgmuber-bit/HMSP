from django.contrib import admin
from .models import Evento, Testimonio, Oracion, Noticia

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'orden_carrusel', 'activo', 'fecha_inicio_publicacion', 'fecha_fin_publicacion')
    list_filter = ('activo', 'fecha')
    search_fields = ('titulo', 'descripcion')
    list_editable = ('orden_carrusel', 'activo')
    prepopulated_fields = {'slug': ('titulo',)}
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'slug', 'descripcion', 'fecha', 'ubicacion', 'imagen')
        }),
        ('Control de Publicación', {
            'fields': ('fecha_inicio_publicacion', 'fecha_fin_publicacion', 'activo', 'orden_carrusel'),
            'description': 'Configure cuándo y cómo se mostrará el evento. El evento se desactivará automáticamente fuera del rango de fechas.'
        }),
        ('Multimedia', {
            'fields': ('tipo_multimedia', 'video_youtube_url', 'video_local', 'preferencia_visualizacion')
        }),
        ('Opciones Adicionales', {
            'fields': ('formulario_url',)
        })
    )

@admin.register(Testimonio)
class TestimonioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'aprobado', 'creado')
    list_filter = ('aprobado', 'creado')
    search_fields = ('nombre', 'testimonio')
    actions = ['aprobar_testimonios', 'rechazar_testimonios']

    def aprobar_testimonios(self, request, queryset):
        queryset.update(aprobado=True)
    aprobar_testimonios.short_description = "Aprobar testimonios seleccionados"

    def rechazar_testimonios(self, request, queryset):
        queryset.update(aprobado=False)
    rechazar_testimonios.short_description = "Rechazar testimonios seleccionados"

@admin.register(Oracion)
class OracionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'activa')
    list_filter = ('categoria', 'activa')
    search_fields = ('titulo', 'contenido')

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'destacada', 'creado')
    list_filter = ('destacada', 'creado')
    search_fields = ('titulo', 'contenido')
    prepopulated_fields = {'slug': ('titulo',)}