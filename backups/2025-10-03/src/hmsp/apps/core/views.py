from django.views.generic import TemplateView, ListView, DetailView
from .models import Evento, Testimonio, Oracion, Noticia

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Eventos para el carrusel (los próximos 5 eventos)
        context['eventos_carrusel'] = Evento.objects.filter(activo=True).order_by('fecha')[:5]
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
        return Evento.objects.filter(activo=True)

class EventoDetailView(DetailView):
    model = Evento
    template_name = 'core/evento_detalle.html'
    context_object_name = 'evento'

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

class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = 'core/noticia_detalle.html'
    context_object_name = 'noticia'