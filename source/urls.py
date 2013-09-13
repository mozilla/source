from django.conf import settings
from django.conf.urls.defaults import patterns, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse

from .base import urls

from funfactory.monkeypatches import patch
patch()

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^browserid/', include('django_browserid.urls')),
    # Generate a robots.txt
    (r'^robots.txt$',
        lambda r: HttpResponse(
            "User-agent: *\n%s: /" % ('Allow' if settings.ENGAGE_ROBOTS else 'Disallow') ,
            mimetype="text/plain"
        )
    ),
    (r'', include(urls)),
)

## In DEBUG mode, serve media files through Django.
if settings.DEBUG:
    # static files
    urlpatterns += staticfiles_urlpatterns()
    # uploaded images
    media_url = settings.MEDIA_URL.lstrip('/').rstrip('/')
    urlpatterns += patterns('',
        (r'^%s/(?P<path>.*)$' % media_url, 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )