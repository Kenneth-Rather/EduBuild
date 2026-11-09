"""WSGI entry point for the EduBuild prototype backend."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edubuild.settings")

application = get_wsgi_application()
