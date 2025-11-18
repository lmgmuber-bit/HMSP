# HMSP - Sistema de Gestión de Contenido Web

Sistema web desarrollado en Django para la gestión y publicación de eventos, noticias, testimonios y oraciones.

## 🚀 Características Principales

### Gestión de Eventos
- **Sistema de programación de publicación**
  - Configuración de fechas de inicio y fin de publicación
  - Desactivación automática de eventos expirados
  - Eventos con publicación indefinida (sin fechas límite)
- **Carrusel dinámico en la página principal**
  - Control manual del orden (posiciones 1-5)
  - Complemento automático con eventos recientes
  - Limpieza automática del carrusel al expirar eventos
- **Soporte multimedia**
  - Imágenes
  - Videos de YouTube (con conversión automática a URL de embed)
  - Videos locales
  - Preferencia de visualización configurable
- **Formularios de inscripción**
  - Integración con Google Forms

### Gestión de Noticias
- Publicación de noticias con imágenes
- Sistema de noticias destacadas
- Slugs automáticos para URLs amigables

### Gestión de Testimonios
- Sistema de aprobación de testimonios
- Acciones masivas desde el panel administrativo
- Soporte para imágenes

### Gestión de Oraciones
- Organización por categorías (Personal, Familia, Sanación, Intercesión)
- Sistema de activación/desactivación

## 🛠️ Tecnologías

- **Backend**: Django 5.2.7
- **Base de datos**: 
  - MySQL (Producción - PythonAnywhere)
  - SQLite3 (Desarrollo local)
- **Frontend**: HTML, CSS, JavaScript
- **Dependencias principales**:
  - python-dotenv
  - gunicorn
  - whitenoise
  - mysqlclient

## 📋 Requisitos Previos

- Python 3.8+
- pip
- virtualenv
- MySQL (para producción)

## 🔧 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/lmgmuber-bit/HMSP.git
cd HMSP
```

### 2. Crear y activar entorno virtual

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear archivo `.env` en la raíz del proyecto:

```env
DJANGO_SECRET_KEY=tu-clave-secreta-aqui
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Crear superusuario

```bash
python manage.py createsuperuser
```

### 7. Recolectar archivos estáticos

```bash
python manage.py collectstatic
```

### 8. Ejecutar servidor de desarrollo

```bash
python manage.py runserver
```

Acceder a:
- Sitio web: http://localhost:8000
- Panel admin: http://localhost:8000/admin

## 📁 Estructura del Proyecto

```
hmsp/
├── hmsp/                       # Configuración del proyecto
│   ├── settings.py            # Configuración principal
│   ├── urls.py                # URLs principales
│   └── apps/
│       ├── core/              # App principal
│       │   ├── models.py      # Modelos de datos
│       │   ├── views.py       # Vistas
│       │   ├── admin.py       # Configuración del admin
│       │   └── urls.py        # URLs de la app
│       └── backoffice/        # Panel administrativo personalizado
├── templates/                 # Plantillas HTML
├── static/                    # Archivos estáticos (CSS, JS, imágenes)
├── media/                     # Archivos subidos por usuarios
├── manage.py                  # Script de gestión de Django
└── requirements.txt           # Dependencias del proyecto
```

## 🎯 Funcionalidades Avanzadas

### Sistema de Publicación Programada

Los eventos pueden programarse para publicación automática:

1. **Sin fechas**: Visible inmediatamente y de forma indefinida
2. **Solo fecha de inicio**: Visible desde esa fecha en adelante
3. **Solo fecha de fin**: Visible hasta esa fecha
4. **Ambas fechas**: Visible solo dentro del rango especificado

El sistema verifica automáticamente en cada carga de página y desactiva eventos fuera de su periodo de publicación.

### Sistema Inteligente de Carrusel

- Muestra hasta 5 eventos en el carrusel principal
- Prioriza eventos con orden manual (1-5)
- Complementa automáticamente con eventos recientes si faltan
- Evita duplicados entre carrusel y sección de próximos eventos

### Panel Administrativo

Acceso completo a:
- Gestión de eventos con edición en línea del orden
- Aprobación/rechazo masivo de testimonios
- Organización de contenido por categorías
- Vista previa de fechas de publicación

## 🔒 Seguridad

- Variables de entorno para datos sensibles
- CSRF protection habilitado
- Clickjacking protection
- XSS protection
- Configuración específica para producción

## 📝 Utilidades de Datos

El proyecto incluye scripts de utilidad:

- `export_data.py`: Exportar datos de la base de datos
- `fix_json.py`: Corregir encoding de archivos JSON
- `transfer_data.py`: Transferir datos entre bases de datos

## 🚀 Despliegue en Producción

El proyecto está configurado para desplegarse en PythonAnywhere:

1. Configurar variables de entorno en PythonAnywhere
2. Configurar base de datos MySQL
3. Subir archivos del proyecto
4. Aplicar migraciones: `python manage.py migrate`
5. Recolectar estáticos: `python manage.py collectstatic`
6. Configurar WSGI y recargar la aplicación

## 📄 Licencia

Este proyecto es privado y de uso exclusivo.

## 👥 Autor

Luis Miguek Gonzalez 

---

**Última actualización**: Noviembre 2025
