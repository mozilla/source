from django.conf import settings
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404


def paginate(request, queryset, results_per_page=20):
    """
    """
    paginator = Paginator(queryset, results_per_page)

    try:
        page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
        raise Http404("No such page of results!")
        
    return page, paginator
