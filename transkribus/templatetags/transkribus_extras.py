from django import template

from transkribus.config import TRANSKRIBUS_TRANSLATIONS

register = template.Library()


@register.simple_tag
def trp_lang():
    return TRANSKRIBUS_TRANSLATIONS
