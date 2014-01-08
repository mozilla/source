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

# attempt to engage with New Relic...
NEW_RELIC_CONFIG_FILE = getattr(settings, 'NEW_RELIC_CONFIG_FILE', None)
if NEW_RELIC_CONFIG_FILE:
    import newrelic.agent
    newrelic.agent.initialize(NEW_RELIC_CONFIG_FILE)

# load the app
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# vim: ft=python