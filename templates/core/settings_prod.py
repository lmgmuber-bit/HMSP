from hmsp.settings import *
import os

DEBUG = True
ALLOWED_HOSTS = ['hmsp.cl', 'www.hmsp.cl', '72.61.132.193']

# Base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'hmsp_db',
        'USER': 'hmsp_user',
        'PASSWORD': '0308Luis$',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    }
}
CSRF_TRUSTED_ORIGINS = [
    'https://hmsp.cl',
    'https://www.hmsp.cl',
]
# Seguridad
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-cambiar-en-produccion-2024')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'


# Archivos estáticos y media
STATIC_ROOT = '/home/hmsp/proyecto/staticfiles/'
MEDIA_ROOT = '/home/hmsp/proyecto/media/'
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.hostinger.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'contacto@hmsp.cl'
EMAIL_HOST_PASSWORD = 'At6TJigY?jQ&Dqx'
DEFAULT_FROM_EMAIL = 'contacto@hmsp.cl'
