from django.conf import settings


def http_protocol(request):
    """
    To stop disqus going bonkers we need to use the same protocal as the domain
    """
    protocol = getattr(settings, 'HTTP_PROTOCOL', False)

    return {
        'HTTP_PROTOCOL': protocol,
    }
