from django.views.generic import TemplateView, ListView, DetailView
from .models import Evento, Testimonio, Oracion, Noticia
import re

def get_youtube_embed_url(url):
    """Convierte una URL de YouTube en una URL de embebido."""
    if not url:
        return ''
        
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([a-zA-Z0-9_-]{11})',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            video_id = match.group(1)
            return f'https://www.youtube.com/embed/{video_id}?rel=0&showinfo=0'
    return url

def verificar_eventos_expirados():
    """Verifica y actualiza el estado de los eventos según sus fechas de publicación"""
    from django.utils import timezone
    from django.db.models import Q
    
    now = timezone.now()
    
    # Buscar eventos que deberían estar inactivos
    eventos_expirados = Evento.objects.filter(
        Q(fecha_fin_publicacion__lt=now) |  # Eventos que han expirado
        Q(fecha_inicio_publicacion__gt=now)  # Eventos que aún no deben estar activos
    ).filter(
        Q(activo=True) | Q(orden_carrusel__gt=0)  # Solo actualizar si están activos o tienen orden en carrusel
    )
    
    # Actualizar eventos expirados
    eventos_expirados.update(activo=False, orden_carrusel=0)

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Verificar eventos expirados antes de mostrarlos
        verificar_eventos_expirados()
        
        # Obtener primero los eventos ordenados
        eventos_ordenados = Evento.objects.filter(
            activo=True,
            orden_carrusel__gt=0
        ).order_by('orden_carrusel', 'fecha')
        
        # Si no hay suficientes eventos ordenados (menos de 5), complementar con los más recientes
        if eventos_ordenados.count() < 5:
            # Obtener los IDs de los eventos ya ordenados para excluirlos
            eventos_ordenados_ids = eventos_ordenados.values_list('id', flat=True)
            
            # Obtener eventos adicionales por fecha, excluyendo los que ya están ordenados
            eventos_adicionales = Evento.objects.filter(
                activo=True,
                orden_carrusel=0
            ).exclude(
                id__in=eventos_ordenados_ids
            ).order_by('-fecha')[:5 - eventos_ordenados.count()]
            
            # Combinar los eventos ordenados con los adicionales
            eventos_carrusel = list(eventos_ordenados) + list(eventos_adicionales)
        else:
            # Si hay 5 o más eventos ordenados, usar solo esos
            eventos_carrusel = eventos_ordenados[:5]
        
        # Procesar las URLs de YouTube para cada evento
        for evento in eventos_carrusel:
            if evento.tipo_multimedia == 'video_youtube' and evento.video_youtube_url:
                evento.video_youtube_url = get_youtube_embed_url(evento.video_youtube_url)
                if evento.video_youtube_url.startswith('https://www.youtube.com/embed/'):
                    video_id = evento.video_youtube_url.split('/')[-1].split('?')[0]
                    evento.video_youtube_url = f'https://www.youtube.com/embed/{video_id}'
        
        context['eventos_carrusel'] = eventos_carrusel
        # Obtener los IDs de todos los eventos que están en el carrusel
        eventos_carrusel_ids = [evento.id for evento in eventos_carrusel]
        
        # Eventos para las tarjetas (excluyendo los que están en el carrusel)
        eventos_proximos = Evento.objects.filter(
            activo=True
        ).exclude(
            id__in=eventos_carrusel_ids
        ).order_by('-fecha')[:3]
        
        context['eventos_proximos'] = eventos_proximos
        context['testimonios_recientes'] = Testimonio.objects.filter(aprobado=True)[:3]
        # Noticias recientes
        context['noticias_recientes'] = Noticia.objects.all().order_by('-creado')[:4]
        return context

class EventoListView(ListView):
    model = Evento
    template_name = 'core/eventos.html'
    context_object_name = 'eventos'
    
    def get_queryset(self):
        # Verificar eventos expirados antes de mostrar la lista
        verificar_eventos_expirados()
        return super().get_queryset()
    paginate_by = 9

    def get_queryset(self):
        queryset = Evento.objects.filter(activo=True)
        
        # Búsqueda por título
        titulo = self.request.GET.get('titulo')
        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
            
        # Búsqueda por rango de fechas
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        
        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)
            
        return queryset.order_by('fecha')

class EventoDetailView(DetailView):
    model = Evento
    template_name = 'core/evento_detalle.html'
    context_object_name = 'evento'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        evento = context['evento']
        
        if evento.tipo_multimedia == 'video_youtube' and evento.video_youtube_url:
            evento.video_youtube_url = get_youtube_embed_url(evento.video_youtube_url)
            
        return context

class TestimonioListView(ListView):
    model = Testimonio
    template_name = 'core/testimonios.html'
    context_object_name = 'testimonios'
    paginate_by = 6

    def get_queryset(self):
        return Testimonio.objects.filter(aprobado=True)

class OracionListView(ListView):
    model = Oracion
    template_name = 'core/oraciones.html'
    context_object_name = 'oraciones'

    def get_queryset(self):
        categoria = self.request.GET.get('categoria')
        if categoria:
            return Oracion.objects.filter(activa=True, categoria=categoria)
        return Oracion.objects.filter(activa=True)

class NoticiaListView(ListView):
    model = Noticia
    template_name = 'core/noticias.html'
    context_object_name = 'noticias'
    paginate_by = 9

    def get_queryset(self):
        queryset = Noticia.objects.all()
        
        # Búsqueda por título
        titulo = self.request.GET.get('titulo')
        if titulo:
            queryset = queryset.filter(titulo__icontains=titulo)
            
        # Búsqueda por rango de fechas
        fecha_desde = self.request.GET.get('fecha_desde')
        fecha_hasta = self.request.GET.get('fecha_hasta')
        
        if fecha_desde:
            queryset = queryset.filter(creado__date__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(creado__date__lte=fecha_hasta)
            
        return queryset.order_by('-creado')

class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = 'core/noticia_detalle.html'
    context_object_name = 'noticia'