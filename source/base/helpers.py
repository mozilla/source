import datetime
import logging
import os
from functools import wraps

from django.conf import settings
from django.template.defaultfilters import linebreaks as django_linebreaks,\
    escapejs as django_escapejs, pluralize as django_pluralize

from jingo import register
from jinja2 import Markup
from sorl.thumbnail import get_thumbnail
from typogrify.filters import typogrify as dj_typogrify

logger = logging.getLogger('base.helpers')

@register.filter
def typogrify(string):
    return Markup(dj_typogrify(string))

@register.filter
def linebreaks(string):
    return django_linebreaks(string)

@register.filter
def escapejs(string):
    return django_escapejs(string)

@register.function
def get_timestamp():
    return datetime.datetime.now()
    
@register.filter
def dj_pluralize(string, arg='s'):
    return django_pluralize(string, arg)

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

