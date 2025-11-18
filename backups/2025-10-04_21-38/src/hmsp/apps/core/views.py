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

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Eventos para el carrusel (los próximos 5 eventos)
        eventos_carrusel = Evento.objects.filter(activo=True).order_by('fecha')[:5]
        
        # Procesar las URLs de YouTube para cada evento
        for evento in eventos_carrusel:
            if evento.tipo_multimedia == 'video_youtube' and evento.video_youtube_url:
                evento.video_youtube_url = get_youtube_embed_url(evento.video_youtube_url)
                if evento.video_youtube_url.startswith('https://www.youtube.com/embed/'):
                    video_id = evento.video_youtube_url.split('/')[-1].split('?')[0]
                    evento.video_youtube_url = f'https://www.youtube.com/embed/{video_id}'
        
        context['eventos_carrusel'] = eventos_carrusel
        # Eventos para las tarjetas (excluyendo los del carrusel)
        context['eventos_proximos'] = Evento.objects.filter(activo=True).order_by('fecha')[5:8]
        context['testimonios_recientes'] = Testimonio.objects.filter(aprobado=True)[:3]
        # Noticias recientes
        context['noticias_recientes'] = Noticia.objects.all().order_by('-creado')[:4]
        return context

class EventoListView(ListView):
    model = Evento
    template_name = 'core/eventos.html'
    context_object_name = 'eventos'
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