# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

from funfactory.settings_base import *

# Name of the top-level module where you put all your apps.
# If you did not install Playdoh with the funfactory installer script
# you may need to edit this value. See the docs about installing from a
# clone.
PROJECT_MODULE = 'source'

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the minify app.
MINIFY_BUNDLES = {
    'css': {
        'sourceapp_css': (
            'css/bootstrap.css',
            'css/font-awesome.css',
            'css/app.css',
        ),
    },
    'js': {
        'sourceapp_js': (
            'js/app.js',
        ),
    }
}

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
    'caching',
    'haystack',
    'sorl.thumbnail',
    'south',
    'taggit',
]

SUPPORTED_NONLOCALES = ['media', 'admin',]

STATIC_URL = '/static/'

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

# sorl-thumbnail settings
DEFAULT_IMAGE_SRC = '/img/uploads/missing.png'

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

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['lhtml'] = [
#    ('**/templates/**.lhtml',
#        'tower.management.commands.extract.extract_tower_template'),
# ]

# # Use this if you have localizable JS files:
# DOMAIN_METHODS['javascript'] = [
#    # Make sure that this won't pull in strings from external libraries you
#    # may use.
#    ('media/js/**.js', 'javascript'),
# ]

LOGGING = dict(loggers=dict(playdoh = {'level': logging.DEBUG}))
