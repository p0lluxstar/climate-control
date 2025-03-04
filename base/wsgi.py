"""
WSGI config for base project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
# from display.fetch_and_store_data import fetch_and_store_data

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'base.settings')

application = get_wsgi_application()
# fetch_and_store_data()
