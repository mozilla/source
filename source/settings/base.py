# Project's main settings file that can be committed to your repo.
# To override a setting locally, use settings/local.py

from funfactory.settings_base import *

# Name of the top-level module where you put all your apps.
PROJECT_MODULE = 'source'

# Defines the views served for root URLs.
ROOT_URLCONF = '%s.urls' % PROJECT_MODULE

INSTALLED_APPS = list(INSTALLED_APPS) + [
    '%s.base' % PROJECT_MODULE,
    '%s.articles' % PROJECT_MODULE,
    '%s.code' % PROJECT_MODULE,
    '%s.jobs' % PROJECT_MODULE,
    '%s.people' % PROJECT_MODULE,
    '%s.tags' % PROJECT_MODULE,
    'caching',
    'haystack',
    'sorl.thumbnail',
    'south',
    'taggit',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.sites',
]

TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS) + [
    'source.base.context_processors.http_protocol',
    'source.base.context_processors.warnr',
]

MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
MIDDLEWARE_CLASSES.append('django.contrib.flatpages.middleware.FlatpageFallbackMiddleware')
# Responsive design means we can remove mobility helpers
MIDDLEWARE_CLASSES = filter(lambda middleware: 'mobility' not in middleware, MIDDLEWARE_CLASSES)

CACHE_MIDDLEWARE_SECONDS = 60*15
FEED_CACHE_SECONDS = 60*15

# Search with django-haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

# Jinja2 is the default template loader. Add any non-Jinja templated apps here:
JINGO_EXCLUDE_APPS = [
    'admin',
    'registration',
]

# dev is under https and live is (currently) on http
# make sure we embed the disqus code with the right protocol
HTTP_PROTOCOL = 'http'

# sorl-thumbnail settings
DEFAULT_IMAGE_SRC = 'img/missing.png'

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS['messages'] = [
    ('%s/**.py' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_python'),
    ('%s/**/templates/**.html' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_template'),
    ('templates/**.html',
        'tower.management.commands.extract.extract_tower_template'),
],

# Should robots.txt deny everything or disallow a calculated list of URLs we
# don't want to be crawled?  Default is false, disallow everything.
# Also see http://www.google.com/support/webmasters/bin/answer.py?answer=93710
ENGAGE_ROBOTS = False

LOGGING = dict(loggers=dict(playdoh={'level': logging.DEBUG}))
