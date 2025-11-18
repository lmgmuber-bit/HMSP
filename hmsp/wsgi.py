"""
WSGI config for hmsp project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hmsp.settings')

application = get_wsgi_application()