from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('eventos/', views.EventoListView.as_view(), name='eventos'),
    path('eventos/<slug:slug>/', views.EventoDetailView.as_view(), name='evento_detalle'),
    path('testimonios/', views.TestimonioListView.as_view(), name='testimonios'),
    path('oraciones/', views.OracionListView.as_view(), name='oraciones'),
    path('noticias/', views.NoticiaListView.as_view(), name='noticias'),
    path('noticias/<slug:slug>/', views.NoticiaDetailView.as_view(), name='noticia_detalle'),
]