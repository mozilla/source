from django.http import HttpResponse
from django.utils import simplejson
from django.utils.functional import lazy, Promise
from django.utils.encoding import force_unicode

class LazyEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        return obj

def render_json_to_response(context):
    result = simplejson.dumps(context, cls=LazyEncoder)
    return HttpResponse(result, mimetype='application/javascript')
