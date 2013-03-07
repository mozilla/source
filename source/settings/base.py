# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

from funfactory.settings_base import *

# Name of the top-level module where you put all your apps.
# If you did not install Playdoh with the funfactory installer script
# you may need to edit this value. See the docs about installing from a
# clone.
PROJECT_MODULE = 'source'

# Defines the views served for root URLs.
ROOT_URLCONF = '%s.urls' % PROJECT_MODULE

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'django.contrib.admin',
    'django.contrib.flatpages',
    'django.contrib.sites',
    '%s.base' % PROJECT_MODULE,
    '%s.articles' % PROJECT_MODULE,
    '%s.code' % PROJECT_MODULE,
    '%s.people' % PROJECT_MODULE,
    '%s.tags' % PROJECT_MODULE,
    'caching',
    'haystack',
    'sorl.thumbnail',
    'south',
    'taggit',
]

TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS) + [
    'source.base.context_processors.http_protocol',
    'source.base.context_processors.warnr',
]

# Adding to standard funfactory middleware classes. Need to insert the
# UpdateCacheMiddleware early on, then append FetchFromCacheMiddleware
MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
MIDDLEWARE_CLASSES.insert(2, 'django.middleware.cache.UpdateCacheMiddleware')
MIDDLEWARE_CLASSES.append('django.contrib.flatpages.middleware.FlatpageFallbackMiddleware')
MIDDLEWARE_CLASSES.append('django.middleware.cache.FetchFromCacheMiddleware')

CACHE_MIDDLEWARE_SECONDS = 120

# Search with django-haystack
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}

# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
JINGO_EXCLUDE_APPS = [
    'admin',
    'registration',
]

# dev is under https and live is (currently) only on http - quick hack to ensure
# we embed the disqus code from the right protocol
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
