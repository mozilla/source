from django.template.defaultfilters import linebreaks as django_linebreaks

from jingo import register

@register.filter
def linebreaks(string):
    return django_linebreaks(string)