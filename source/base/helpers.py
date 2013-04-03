import datetime
import logging
import os

from django.conf import settings
from django.template.defaultfilters import linebreaks as django_linebreaks,\
    escapejs as django_escapejs

from jingo import register
from sorl.thumbnail import get_thumbnail

logger = logging.getLogger('base.helpers')

@register.filter
def linebreaks(string):
    return django_linebreaks(string)

@register.filter
def escapejs(string):
    return django_escapejs(string)

@register.function
def get_timestamp():
    return datetime.datetime.now()

@register.function
def thumbnail(source, *args, **kwargs):
    """
    Wraps sorl thumbnail with an additional 'default' keyword
    https://github.com/mozilla/mozillians/blob/master/apps/common/helpers.py
    """

    # Templates should never return an exception
    try:
        if not source.path:
            source = kwargs.get('default')

        # Handle PNG images a little more gracefully
        # Make sure thumbnail call doesn't specifically set format
        if not 'format' in kwargs:
            filetype = source.path.split('.')[-1]
            # If we have a PNG, don't default convert to JPG
            if filetype.lower() == 'png':
                kwargs['format'] = 'PNG'
        
        return get_thumbnail(source, *args, **kwargs)
    except Exception as e:
        logger.error('Thumbnail had Exception: %s' % (e,))
        source = getattr(settings, 'DEFAULT_IMAGE_SRC')
        return get_thumbnail(source, *args, **kwargs)
