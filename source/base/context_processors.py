from django.conf import settings


def http_protocol(request):
    """
    To stop disqus going bonkers we need to use the same protocal as the domain
    """
    protocol = getattr(settings, 'HTTP_PROTOCOL', False)

    return {
        'HTTP_PROTOCOL': protocol,
    }


def warnr(request):
    """
    As we're using an external service to resize images we need to pipe through
    the FULL domain - https:// and everything
    """

    stage = getattr(settings, 'APP_STAGE', False)
    message = getattr(settings, 'APP_MESSAGE', False)

    return {
        'APP_STAGE': stage,
        'APP_MSG': message
    }
