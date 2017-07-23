from django import template
from django.template.defaultfilters import stringfilter
from tobaccopoisk import utils

register = template.Library()

@register.filter
@stringfilter
def real_url(s):
    return utils.image_url_handler(s)

@register.filter
@stringfilter
def view_str(s):
    return utils.to_view_str(s)
