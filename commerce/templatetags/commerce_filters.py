from decimal import Decimal
import string
from unicodedata import decimal
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_str


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

@register.filter
@stringfilter
def aggiungiCosti(value,arg):
    return Decimal(Decimal(value)+Decimal(arg))


@register.filter
def intdot(val_orig):  
    
    return force_str(val_orig).replace(',', '.')