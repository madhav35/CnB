from django import template

register = template.Library()

@register.filter(name='endswith')
def endswith(value, suffix):
    return value.lower().endswith(suffix.lower())

@register.filter(name='split_services')  # Registering the split_services filter
def split_services(value, delimiter=','):
    """Split the services string into a list based on the given delimiter."""
    if value:
        return value.split(delimiter)
    return []
