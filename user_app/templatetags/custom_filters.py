from django import template

register = template.Library()


@register.filter(name='trim_media')
def trim_media(value):
    """Removes '/home' from the start of the URL."""
    if value.startswith('/media'):
        return value[len('/media'):]
    return value
