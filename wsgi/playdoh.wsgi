import os
import site

newrelic_cfg_file = os.environ.get('NEW_RELIC_CONFIG_FILE')

if newrelic_cfg_file:
    import newrelic.agent
    newrelic.agent.initialize(newrelic_cfg_file,
                              os.environ.get('NEW_RELIC_ENVIRONMENT'))
    newrelic_settings = newrelic.agent.global_settings()
                        
os.environ.setdefault('CELERY_LOADER', 'django')
# NOTE: you can also set DJANGO_SETTINGS_MODULE in your environment to override
# the default value in manage.py

# Add the app dir to the python path so we can import manage.
wsgidir = os.path.dirname(__file__)
site.addsitedir(os.path.abspath(os.path.join(wsgidir, '../')))

# manage adds /apps, /lib, and /vendor to the Python path.
import manage

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

if newrelic_cfg_file:
    application = newrelic.agent.wsgi_application()(application)

# vim: ft=python
