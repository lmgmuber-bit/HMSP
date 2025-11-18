import pytest
from django.urls import reverse
from django.test import Client
from .models import Evento, Testimonio, Oracion, Noticia
from datetime import datetime, timedelta

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def evento_futuro():
    return Evento.objects.create(
        titulo='Evento de Prueba',
        descripcion='Descripción del evento de prueba',
        fecha=datetime.now() + timedelta(days=7),
        activo=True
    )

@pytest.fixture
def testimonio_aprobado():
    return Testimonio.objects.create(
        nombre='Juan Pérez',
        testimonio='Este es un testimonio de prueba',
        aprobado=True
    )

@pytest.mark.django_db
class TestViews:
    def test_home_view(self, client):
        response = client.get(reverse('core:home'))
        assert response.status_code == 200
        assert 'eventos_proximos' in response.context
        assert 'testimonios_recientes' in response.context
        assert 'noticias_destacadas' in response.context

    def test_evento_list_view(self, client, evento_futuro):
        response = client.get(reverse('core:eventos'))
        assert response.status_code == 200
        assert evento_futuro in response.context['eventos']

    def test_evento_detail_view(self, client, evento_futuro):
        response = client.get(reverse('core:evento_detalle', kwargs={'slug': evento_futuro.slug}))
        assert response.status_code == 200
        assert response.context['evento'] == evento_futuro

    def test_testimonio_list_view(self, client, testimonio_aprobado):
        response = client.get(reverse('core:testimonios'))
        assert response.status_code == 200
        assert testimonio_aprobado in response.context['testimonios']

@pytest.mark.django_db
class TestModels:
    def test_evento_str(self, evento_futuro):
        assert str(evento_futuro) == evento_futuro.titulo

    def test_testimonio_str(self, testimonio_aprobado):
        assert str(testimonio_aprobado) == f"Testimonio de {testimonio_aprobado.nombre}"

    def test_evento_slug_generation(self):
        evento = Evento.objects.create(
            titulo='Título con Espacios',
            descripcion='Descripción de prueba',
            fecha=datetime.now() + timedelta(days=1)
        )
        assert evento.slug == 'titulo-con-espacios'

@pytest.mark.django_db
class TestForms:
    def test_testimonio_creation(self):
        testimonio = Testimonio.objects.create(
            nombre='Ana García',
            testimonio='Un nuevo testimonio',
            aprobado=False
        )
        assert not testimonio.aprobado
        assert Testimonio.objects.count() == 1