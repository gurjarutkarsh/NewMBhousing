"""
WSGI config for MBInventoryTool project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

#from MBInventoryTool.wsgi import MBInventoryToolApplication

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MBInventoryTool.settings')

application = get_wsgi_application()

#application = MBInventoryToolApplication(application)


"""
from helloworld.wsgi import HelloWorldApplication

application = HelloWorldApplication(application)
"""