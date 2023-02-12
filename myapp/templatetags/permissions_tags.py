from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escapejs

import json

register = template.Library()


@register.filter(name='has_role')
def has_role(user, names):
    role_names = names.split(',')
    if hasattr(user, 'groups'):
        if user.groups.filter(name__in=role_names).exists():
            return True
    return False


@register.filter(name='difference')
def difference(minuendo, sustraendo):
    return minuendo - sustraendo


@register.filter
def to_js(value):
    """
    To use a python variable in JS, we call json.dumps to serialize as JSON server-side and reconstruct using
    JSON.parse. The serialized string must be escaped appropriately before dumping into the client-side code.
    """
    # separators is passed to remove whitespace in output
    return mark_safe('JSON.parse("%s")' % escapejs(json.dumps(value, separators=(',', ':'))))
