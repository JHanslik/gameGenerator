from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """
    Divise une chaîne de caractères selon un délimiteur spécifié
    Usage: {{ value|split:"," }}
    """
    return value.split(arg)

@register.filter
def trim(value):
    """
    Enlève les espaces au début et à la fin d'une chaîne
    Usage: {{ value|trim }}
    """
    return value.strip() if value else value
