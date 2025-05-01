from django import template
import re

register = template.Library()

@register.simple_tag
def active_class(request, pattern):
    if re.fullmatch(pattern, request.path):
        return 'active'
    return ''
