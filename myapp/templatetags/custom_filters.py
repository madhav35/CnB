from django import template

register = template.Library()

@register.filter(name='endswith')
def endswith(value, suffix):
    return value.lower().endswith(suffix.lower())
