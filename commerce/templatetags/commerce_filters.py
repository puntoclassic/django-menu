from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def endswith(value, arg):
    return value.endswith(arg)

@register.filter
@stringfilter
def contains(value, arg):
    return value.find(arg) != -1

@register.filter
@stringfilter
def startswith(value, arg):
    return value.startswith(arg)