# Vista pública para la guía del administrador
def guia_admin(request):
    return render(request, 'core/guia_admin.html')
# Vista pública para la guía del usuario
from django.shortcuts import render
def guia_usuario(request):
    return render(request, 'core/guia_usuario.html')
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Suscripcion
# Vista para cancelar suscripción automáticamente
def cancelar_suscripcion_auto(request):
    email = request.GET.get('email')
    if email:
        suscripcion = Suscripcion.objects.filter(email=email).first()
        if suscripcion:
            suscripcion.delete()
            return render(request, 'core/cancelar_confirmacion.html', {'email': email})
        else:
            return render(request, 'core/cancelar_confirmacion.html', {'email': email, 'not_found': True})
    return HttpResponse('Solicitud inválida', status=400)
# --- Cancelar suscripción ---
from django.http import HttpResponseRedirect
from django.contrib import messages
def cancelar_suscripcion(request):
    from .models import Suscripcion
    email = request.GET.get('email')
    if email:
        Suscripcion.objects.filter(email=email).delete()
        messages.success(request, 'Tu suscripción ha sido cancelada correctamente.')
    return HttpResponseRedirect('/')
# Vista de previsualización de correo


def email_preview(request):
    from .models import ConfiguracionSitio, Evento
    config = ConfiguracionSitio.objects.first()
    logo_url = config.logo_principal.url if config and config.logo_principal else None
    suscriptor = {'nombre': 'Juan Pérez'}
    # Buscar un evento real con imagen
    evento = Evento.objects.filter(imagen__isnull=False).order_by('-fecha').first()
    if evento:
        ejemplo = {
            'titulo': evento.titulo,
            'imagen_url': f'https://hmsp.cl{evento.imagen.url}' if evento.imagen else '',
            'fecha': evento.fecha.strftime('%d/%m/%Y %H:%M'),
            'ubicacion': evento.ubicacion,
            'descripcion': evento.descripcion,
            'url': f'https://hmsp.cl/eventos/{evento.slug}/',
            'suscriptor': suscriptor,
            'logo_url': logo_url
        }
    else:
        ejemplo = {
            'titulo': 'Retiro Espiritual HMSP',
            'imagen_url': 'https://hmsp.cl/static/img/ejemplo-evento.jpg',
            'fecha': '25/11/2025 18:00',
            'ubicacion': 'Parroquia San Pablo',
            'descripcion': 'Te invitamos al retiro espiritual anual. Habrá charlas, oración y convivencia.',
            'url': 'https://hmsp.cl/eventos/retiro-espiritual-hmsp/',
            'suscriptor': suscriptor,
            'logo_url': logo_url
        }
    return render(request, 'core/email_preview.html', ejemplo)

# Previsualización de correo para evento con video
def email_preview_video(request):
    from .models import ConfiguracionSitio, Evento
    config = ConfiguracionSitio.objects.first()
    logo_url = config.logo_principal.url if config and config.logo_principal else None
    suscriptor = {'nombre': 'Juan Pérez'}
    evento = Evento.objects.filter(tipo_multimedia__in=['video_youtube', 'video_local']).order_by('-fecha').first()
    video_url = None
    if evento:
        if evento.tipo_multimedia == 'video_youtube' and evento.video_youtube_url:
            video_url = evento.get_youtube_embed_url()
        elif evento.tipo_multimedia == 'video_local' and evento.video_local:
            video_url = evento.video_local.url
        ejemplo = {
            'titulo': evento.titulo,
            'imagen_url': f'https://hmsp.cl{evento.imagen.url}' if evento.imagen else '',
            'fecha': evento.fecha.strftime('%d/%m/%Y %H:%M'),
            'ubicacion': evento.ubicacion,
            'descripcion': evento.descripcion,
            'url': f'https://hmsp.cl/eventos/{evento.slug}/',
            'suscriptor': suscriptor,
            'logo_url': logo_url,
            'video_url': video_url,
            'tipo_multimedia': evento.tipo_multimedia
        }
    else:
        ejemplo = {
            'titulo': 'Evento con Video',
            'imagen_url': '',
            'fecha': '25/11/2025 18:00',
            'ubicacion': 'Parroquia San Pablo',
            'descripcion': 'Ejemplo de evento con video YouTube o local.',
            'url': 'https://hmsp.cl/eventos/ejemplo-video/',
            'suscriptor': suscriptor,
            'logo_url': logo_url,
            'video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ',
            'tipo_multimedia': 'video_youtube'
        }
    return render(request, 'core/email_preview_video.html', ejemplo)

from django.views.generic import TemplateView, ListView, DetailView
from .models import Evento, Testimonio, Oracion, Noticia, ConfiguracionSitio, Apostolado, Suscripcion
from .forms import SuscripcionForm
from django.shortcuts import render, redirect
from django.contrib import messages
import re
from django.db.models import Q
from django.utils import translation
from django.conf import settings

# Vista para suscripción de usuarios

def suscripcion_view(request):
    from django.http import JsonResponse
    if request.method == 'POST':
        form = SuscripcionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if Suscripcion.objects.filter(email=email).exists():
                msg = 'Correo suscrito.'
                status = 'info'
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'message': msg, 'status': status})
                else:
                    messages.info(request, msg)
                    return redirect('core:suscripcion')
            else:
                form.save()
                msg = '¡Te has suscrito correctamente!'
                status = 'success'
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'message': msg, 'status': status})
                else:
                    messages.success(request, msg)
                    return redirect('core:suscripcion')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Mostrar error específico si existe en el campo email
                email_errors = form.errors.get('email')
                telefono_errors = form.errors.get('telefono')
                nombre_errors = form.errors.get('nombre')
                if email_errors:
                    msg = email_errors[0]
                elif telefono_errors:
                    msg = telefono_errors[0]
                elif nombre_errors:
                    msg = nombre_errors[0]
                else:
                    msg = 'Formulario inválido. Verifica los datos.'
                return JsonResponse({'message': msg, 'status': 'error'})
    else:
        form = SuscripcionForm()
    return render(request, 'core/suscripcion.html', {'form': form})

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
        # Testimonios destacados (filtrar por aprobado=True, destacado=True y orden > 0)
        context['testimonios_destacados'] = Testimonio.objects.filter(
            aprobado=True,
            destacado=True,
            orden_destacado__gt=0
        ).order_by('orden_destacado')[:3]
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

class QuienesSomosView(TemplateView):
    template_name = 'core/quienes_somos.html'


class RecursosView(TemplateView):
    template_name = 'core/recursos.html'


class ContactoView(TemplateView):
    template_name = 'core/contacto.html'
    
    def post(self, request, *args, **kwargs):
        from .models import MensajeContacto
        from django.contrib import messages
        from django.shortcuts import redirect
        from django.utils.html import escape
        import re
        
        # Obtener y sanitizar datos del formulario
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip()
        asunto = request.POST.get('asunto', '').strip()
        mensaje = request.POST.get('mensaje', '').strip()
        
        # Validar que todos los campos estén presentes
        if not all([nombre, email, asunto, mensaje]):
            messages.error(request, 'Por favor completa todos los campos del formulario.')
            return redirect('core:contacto')
        
        # Validar longitud de campos
        if len(nombre) > 200 or len(email) > 254 or len(asunto) > 200 or len(mensaje) > 5000:
            messages.error(request, 'Uno o más campos exceden la longitud máxima permitida.')
            return redirect('core:contacto')
        
        # Validar formato de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messages.error(request, 'Por favor ingresa un correo electrónico válido.')
            return redirect('core:contacto')
        
        # Detectar caracteres sospechosos o palabras SQL peligrosas
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 
                       'EXEC', 'EXECUTE', 'SCRIPT', 'UNION', '--', '/*', '*/', ';--', 'xp_']
        
        combined_text = f"{nombre} {asunto} {mensaje}".upper()
        if any(keyword in combined_text for keyword in sql_keywords):
            messages.error(request, 'El mensaje contiene contenido no permitido. Por favor revisa tu texto.')
            return redirect('core:contacto')
        
        # Sanitizar datos (escape HTML para prevenir XSS)
        nombre_sanitizado = escape(nombre)
        asunto_sanitizado = escape(asunto)
        mensaje_sanitizado = escape(mensaje)
        
        try:
            # Guardar el mensaje en la base de datos usando ORM (protegido contra SQL injection)
            MensajeContacto.objects.create(
                nombre=nombre_sanitizado,
                email=email.lower(),  # Normalizar email a minúsculas
                asunto=asunto_sanitizado,
                mensaje=mensaje_sanitizado
            )
            messages.success(request, '¡Gracias por contactarnos! Hemos recibido tu mensaje y te responderemos pronto.')
        except Exception as e:
            messages.error(request, 'Ocurrió un error al enviar tu mensaje. Por favor intenta nuevamente.')
        
        return redirect('core:contacto')


class ApostoladoListView(ListView):
    model = Apostolado
    template_name = 'core/apostolados.html'
    context_object_name = 'apostolados'
    
    def get_queryset(self):
        return Apostolado.objects.filter(activo=True).order_by('orden', 'titulo')


class ApostoladoDetailView(DetailView):
    model = Apostolado
    template_name = 'core/apostolado_detalle.html'
    context_object_name = 'apostolado'
    
    def get_queryset(self):
        return Apostolado.objects.filter(activo=True)

class BuscarView(TemplateView):
    template_name = 'core/buscar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        context['query'] = query
        resultados = []
        if query:
            resultados += [self._add_tipo(obj, 'Evento') for obj in Evento.objects.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query), activo=True)]
            resultados += [self._add_tipo(obj, 'Noticia') for obj in Noticia.objects.filter(Q(titulo__icontains=query) | Q(contenido__icontains=query))]
            resultados += [self._add_tipo(obj, 'Testimonio') for obj in Testimonio.objects.filter(Q(nombre__icontains=query) | Q(testimonio__icontains=query))]
            resultados += [self._add_tipo(obj, 'Apostolado') for obj in Apostolado.objects.filter(Q(titulo__icontains=query) | Q(descripcion__icontains=query), activo=True)]
        context['resultados'] = resultados
        return context

    def _add_tipo(self, obj, tipo):
        obj.tipo = tipo
        return obj

class IdiomaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        lang = request.GET.get('lang')
        if lang in dict(settings.LANGUAGES):
            translation.activate(lang)
            request.LANGUAGE_CODE = lang
        response = self.get_response(request)
        translation.deactivate()
        return response