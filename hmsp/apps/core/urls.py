from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('quienes-somos/', views.QuienesSomosView.as_view(), name='quienes_somos'),
    path('recursos/', views.RecursosView.as_view(), name='recursos'),
    path('contacto/', views.ContactoView.as_view(), name='contacto'),
    path('eventos/', views.EventoListView.as_view(), name='eventos'),
    path('eventos/<slug:slug>/', views.EventoDetailView.as_view(), name='evento_detalle'),
    path('testimonios/', views.TestimonioListView.as_view(), name='testimonios'),
    path('oraciones/', views.OracionListView.as_view(), name='oraciones'),
    path('noticias/', views.NoticiaListView.as_view(), name='noticias'),
    path('noticias/<slug:slug>/', views.NoticiaDetailView.as_view(), name='noticia_detalle'),
    path('apostolados/', views.ApostoladoListView.as_view(), name='apostolados'),
    path('apostolados/<slug:slug>/', views.ApostoladoDetailView.as_view(), name='apostolado_detalle'),
    path('buscar/', views.BuscarView.as_view(), name='buscar'),
    path('suscripcion/', views.suscripcion_view, name='suscripcion'),
    path('email-preview/', views.email_preview, name='email_preview'),
    path('email-preview-video/', views.email_preview_video, name='email_preview_video'),
    path('cancelar-suscripcion/', views.cancelar_suscripcion, name='cancelar_suscripcion'),
    path('suscripcion/cancelar/', views.cancelar_suscripcion_auto, name='cancelar_suscripcion_auto'),
    path('guia-usuario/', views.guia_usuario, name='guia_usuario'),
    path('guia-admin/', views.guia_admin, name='guia_admin'),
]