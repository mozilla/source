import datetime
import logging
import os
import re

from django.conf import settings
from django.template.defaultfilters import linebreaks as django_linebreaks,\
    escapejs as django_escapejs, pluralize as django_pluralize,\
    date as django_date
from django.utils.encoding import force_text
from django.utils.timesince import timesince

from jingo import register
from jinja2 import Markup
from sorl.thumbnail import get_thumbnail
from typogrify.filters import typogrify as dj_typogrify,\
    smartypants as dj_smartypants

logger = logging.getLogger('base.helpers')

@register.filter
def typogrify(string):
    return Markup(dj_typogrify(string))

@register.filter
def smartypants(string):
    return Markup(dj_smartypants(string))

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
def dj_date(value, format_string):
    return django_date(value, format_string)

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

@register.filter
def dj_intcomma(value):
    """
    https://github.com/django/django/blob/master/django/contrib/humanize/templatetags/humanize.py
    Converts an integer to a string containing commas every three digits.
    For example, 3000 becomes '3,000' and 45000 becomes '45,000'.
    """
    orig = force_text(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>,\g<2>', orig)
    if orig == new:
        return new
    else:
        return dj_intcomma(new)
        
@register.filter
def simple_timesince(value):
    now = datetime.datetime.now()
    try:
        difference = now - value
    except:
        return value

    if difference <= datetime.timedelta(minutes=1):
        return 'just now'
    return '%(time)s ago' % {'time': timesince(value).split(', ')[0]}
    
@register.filter
def simple_datesince(value):
    today = datetime.datetime.today().date()
    try:
        difference = today - value
    except:
        return value

    if difference <= datetime.timedelta(days=1):
        return 'today'
    return '%(days)s ago' % {'days': timesince(value).split(', ')[0]}
