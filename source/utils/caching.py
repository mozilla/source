import hashlib

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.urlresolvers import resolve
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, Http404
from django.utils import simplejson
from django.utils.cache import get_cache_key
from django.utils.decorators import method_decorator
from django.utils.encoding import iri_to_uri
from django.utils.translation import get_language
from django.views.generic import View

from funfactory import urlresolvers
from .json import LazyEncoder


def expire_page_cache(path, key_prefix=None):
    # pass the path through funfactory resolver in order to get locale
    resolved_path = resolve(path)
    path_with_locale = urlresolvers.reverse(
        resolved_path.func,
        args = resolved_path.args,
        kwargs = resolved_path.kwargs
    )
    try:
        language = urlresolvers.split_path(path_with_locale)[0].lower()
    except:
        language = None

    # get cache key, expire if the cached item exists
    key = get_url_cache_key(
        path_with_locale, language=language, key_prefix=key_prefix
    )

    if key:
        if cache.get(key):
            cache.set(key, None, 0)
        return True
    return False


def get_url_cache_key(url, language=None, key_prefix=None):
    '''
    modified version of http://djangosnippets.org/snippets/2595/
    '''
    if key_prefix is None:
        key_prefix = getattr(settings, 'CACHE_MIDDLEWARE_KEY_PREFIX', None)
    ctx = hashlib.md5()
    path = hashlib.md5(iri_to_uri(url))
    cache_key = 'views.decorators.cache.cache_page.%s.%s.%s.%s' % (
        key_prefix, 'GET', path.hexdigest(), ctx.hexdigest()
    )
    if language:
        cache_key += '.%s' % language
    return cache_key


class ClearCache(View):
    def render_json_to_response(self, context):
        result = simplejson.dumps(context, cls=LazyEncoder)
        return HttpResponse(result, mimetype='application/javascript')

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        path = request.GET.get('path', None)
        
        try:
            resolved_path = resolve(path)
            expire_page_cache(path)
        except:
            raise Http404
        if self.request.is_ajax():
            result = {'success': 'True'}
            return self.render_json_to_response(result)
        else:
            return HttpResponse('Cache cleared for "%s"!' % path)
            
