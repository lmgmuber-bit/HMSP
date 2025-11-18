from django.contrib import admin
from .models import Evento, Testimonio, Oracion, Noticia

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'fecha', 'activo')
    list_filter = ('activo', 'fecha')
    search_fields = ('titulo', 'descripcion')
    prepopulated_fields = {'slug': ('titulo',)}

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