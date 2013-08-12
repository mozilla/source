import os
import site
import sys

# make sure we have the right DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "source.settings")

os.environ.setdefault('CELERY_LOADER', 'django')

# Add the app dir to the python path so we can import manage.
wsgidir = os.path.dirname(__file__)
site.addsitedir(os.path.abspath(os.path.join(wsgidir, '../')))

# manage adds /apps, /lib, and /vendor to the Python path.
import manage
from django.conf import settings

NEW_RELIC_CONFIG_FILE = getattr(settings, 'NEW_RELIC_CONFIG_FILE', None)
NEW_RELIC_ENVIRONMENT = getattr(settings, 'NEW_RELIC_ENVIRONMENT', None)

if NEW_RELIC_CONFIG_FILE and NEW_RELIC_ENVIRONMENT:
    import newrelic.agent
    newrelic.agent.initialize(NEW_RELIC_CONFIG_FILE, NEW_RELIC_ENVIRONMENT)
    newrelic_settings = newrelic.agent.globalsettings()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

if NEW_RELIC_CONFIG_FILE:
    application = newrelic.agent.wsgi_application()(application)

# vim: ft=python