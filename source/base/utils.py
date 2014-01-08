from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404, HttpResponse
from django.utils import simplejson


def paginate(request, queryset, results_per_page=20):
    paginator = Paginator(queryset, results_per_page)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("Sorry, that page of results does not exist.")
    except ValueError:
        raise PermissionDenied()
        
    return page, paginator

def render_json_to_response(context):
    '''
    Utility method for rendering a view's data to JSON response.
    '''
    result = simplejson.dumps(context, sort_keys=False, indent=4)
    return HttpResponse(result, mimetype='application/javascript')
