from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def endswith(value, arg):
    """Verifica se a string termina com a extensão fornecida."""
    return value.endswith(arg)